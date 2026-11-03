"""
LLM-аннотатор для двух задач:

1. Валидация существующих пар — пройти по `annotations.csv`, попросить LLM
   подтвердить или поправить relation. Полезно для шумных классов
   has_property и has_function, где Wikidata-предикат семантически расплывчат.

2. Генерация пар класса `precedes` — для понятий-процессов (митоз, фотосинтез,
   эмбриогенез...) LLM выдаёт упорядоченную последовательность этапов;
   соседние этапы становятся парами `precedes`.

Провайдеры:
  * OpenAICompatibleProvider — работает с OpenAI, vLLM, LM Studio, Ollama (через
    openai-совместимый endpoint). Управляется env vars и аргументами.
  * MockProvider — детерминированные ответы для тестов.

Промпты лежат в annotation/prompts/*.txt и подменяются через .format().

Использование (см. также scripts/llm_annotate.py):

    from mindmap2kg.annotation.llm_annotator import (
        LLMAnnotator, OpenAICompatibleProvider, MockProvider,
    )

    annot = LLMAnnotator(provider=OpenAICompatibleProvider(model="gpt-4o-mini"))
    df_val = annot.validate_pairs(df_existing)
    df_prec = annot.generate_precedes(topics=["митоз", "фотосинтез"])
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent / "prompts"


# =============================================================================
# Провайдеры
# =============================================================================


class BaseLLMProvider(ABC):
    """Абстракция LLM. Принимает строку — возвращает строку."""

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str: ...

    @property
    def name(self) -> str:
        return self.__class__.__name__


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    Работает с любым OpenAI-совместимым API: OpenAI, vLLM, LM Studio,
    Ollama (через /v1), TogetherAI, и т.д.

    Параметры берутся в порядке: аргумент конструктора → env var → default.
      api_key: LLM_API_KEY или OPENAI_API_KEY
      base_url: LLM_BASE_URL или OPENAI_BASE_URL (default: https://api.openai.com/v1)
      model: аргумент или LLM_MODEL (default: gpt-4o-mini)
    """

    def __init__(self,
                 model: str | None = None,
                 api_key: str | None = None,
                 base_url: str | None = None,
                 temperature: float = 0.0,
                 max_tokens: int = 512,
                 timeout: float = 60.0,
                 max_retries: int = 3):
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = (base_url
                         or os.getenv("LLM_BASE_URL")
                         or os.getenv("OPENAI_BASE_URL")
                         or "https://api.openai.com/v1")
        if not self.api_key:
            raise RuntimeError(
                "Нет API-ключа. Установи LLM_API_KEY или OPENAI_API_KEY "
                "(или передай api_key= в конструктор).")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

    def complete(self, prompt: str, **kwargs) -> str:
        import requests

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens":  kwargs.get("max_tokens",  self.max_tokens),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(self.max_retries):
            try:
                r = requests.post(url, headers=headers, json=payload,
                                  timeout=self.timeout)
                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"]
                if r.status_code in (429, 500, 502, 503, 504):
                    wait = 2 ** attempt
                    logger.warning("HTTP %s, повтор через %ss", r.status_code, wait)
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"LLM HTTP {r.status_code}: {r.text[:300]}")
            except requests.RequestException as e:
                logger.warning("Сетевая ошибка: %s (попытка %d)", e, attempt + 1)
                time.sleep(2 ** attempt)
        raise RuntimeError("Превышено число попыток обращения к LLM")


class MockProvider(BaseLLMProvider):
    """
    Детерминированный мок для тестов.

    Стратегия ответов:
      * Если промпт содержит "validate_pair"-маркер (текст шаблона) — возвращает
        verdict=correct.
      * Если промпт содержит "generate_precedes"-маркер — возвращает 4 этапа.
    Определение маркера — по характерным словам шаблонов.
    """

    def __init__(self, validate_verdict: str = "correct",
                 precedes_stages: list[str] | None = None,
                 suggested: str | None = None):
        self.validate_verdict = validate_verdict
        self.precedes_stages = precedes_stages or [
            "первый этап", "второй этап", "третий этап", "четвёртый этап"
        ]
        self.suggested = suggested

    def complete(self, prompt: str, **kwargs) -> str:
        if "Перечисли последовательные этапы" in prompt or "stages" in prompt:
            return json.dumps({
                "is_sequential": True,
                "stages": self.precedes_stages,
            }, ensure_ascii=False)
        # default — валидация
        payload = {
            "verdict": self.validate_verdict,
            "suggested_relation": self.suggested or "",
            "rationale": "mock",
        }
        return json.dumps(payload, ensure_ascii=False)


# =============================================================================
# Парсинг ответов LLM
# =============================================================================


_JSON_RE = re.compile(r"\{[\s\S]*\}")


def _extract_json(text: str) -> dict | None:
    """Достать первый JSON-объект из ответа LLM, терпимо к ```json фенсам."""
    text = text.strip()
    # снять markdown-фенсы
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = _JSON_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# =============================================================================
# Аннотатор
# =============================================================================


@dataclass
class ValidationResult:
    verdict: str               # "correct" | "wrong" | "uncertain"
    suggested_relation: str    # "" если verdict=correct
    rationale: str
    raw: str                   # сырой ответ LLM на всякий случай


class LLMAnnotator:
    KNOWN_RELATIONS = {
        "has_part", "has_example", "has_property", "has_function",
        "causes", "precedes", "associated_with",
    }

    def __init__(self, provider: BaseLLMProvider,
                 prompts_dir: Path | str = PROMPTS_DIR,
                 sleep_between: float = 0.0):
        self.provider = provider
        self.prompts_dir = Path(prompts_dir)
        self.sleep_between = sleep_between
        self._templates: dict[str, str] = {}

    def _load_prompt(self, name: str) -> str:
        if name not in self._templates:
            self._templates[name] = (
                self.prompts_dir / f"{name}.txt").read_text(encoding="utf-8")
        return self._templates[name]

    # ---- 1) Валидация существующих пар ------------------------------------

    def validate_pair(self, u_text: str, v_text: str,
                      relation: str) -> ValidationResult:
        tpl = self._load_prompt("validate_pair")
        prompt = tpl.format(u_text=u_text, v_text=v_text, relation=relation)
        raw = self.provider.complete(prompt)
        if self.sleep_between:
            time.sleep(self.sleep_between)

        data = _extract_json(raw) or {}
        verdict = str(data.get("verdict", "uncertain")).lower()
        if verdict not in {"correct", "wrong", "uncertain"}:
            verdict = "uncertain"
        suggested = str(data.get("suggested_relation", "")).strip()
        if suggested and suggested not in self.KNOWN_RELATIONS:
            suggested = ""
        rationale = str(data.get("rationale", "")).strip()
        return ValidationResult(verdict=verdict,
                                suggested_relation=suggested,
                                rationale=rationale,
                                raw=raw)

    def validate_pairs(self, df: pd.DataFrame,
                       only_relations: list[str] | None = None,
                       limit: int | None = None,
                       verbose: bool = True) -> pd.DataFrame:
        """
        Прогоняет валидатор по строкам df.
        Возвращает df с добавленными колонками llm_verdict, llm_suggested,
        llm_rationale, llm_model.

        only_relations: ограничиться этими классами (например, только шумными).
        limit: максимум строк (для пилотного прогона).
        """
        work = df.copy()
        if only_relations:
            mask = work["relation"].isin(only_relations)
        else:
            mask = pd.Series(True, index=work.index)
        if limit:
            target_idx = work[mask].head(limit).index
        else:
            target_idx = work[mask].index

        verdicts: dict[int, ValidationResult] = {}
        total = len(target_idx)
        for i, idx in enumerate(target_idx, 1):
            row = work.loc[idx]
            if verbose:
                print(f"[{i:>4}/{total}] {row['u_text']!r} → {row['v_text']!r} "
                      f"({row['relation']})", end=" ", flush=True)
            try:
                res = self.validate_pair(row["u_text"], row["v_text"],
                                         row["relation"])
                if verbose:
                    print(f"→ {res.verdict}"
                          + (f" / {res.suggested_relation}" if res.suggested_relation else ""))
                verdicts[idx] = res
            except Exception as e:
                if verbose:
                    print(f"ERROR: {e}")
                logger.warning("Ошибка валидации строки %d: %s", idx, e)

        # пишем колонки
        for col in ("llm_verdict", "llm_suggested", "llm_rationale", "llm_model"):
            if col not in work.columns:
                work[col] = ""
        for idx, res in verdicts.items():
            work.at[idx, "llm_verdict"]    = res.verdict
            work.at[idx, "llm_suggested"]  = res.suggested_relation
            work.at[idx, "llm_rationale"]  = res.rationale
            work.at[idx, "llm_model"]      = self.provider.name
        return work

    # ---- 2) Генерация precedes-пар ----------------------------------------

    def generate_precedes(self, topics: list[str],
                          verbose: bool = True) -> pd.DataFrame:
        """
        Для каждого topic запросить упорядоченные этапы и собрать
        соседние в пары (stage_k → stage_{k+1}, relation=precedes).
        Также к каждому topic добавляются пары topic → stage_k с relation=has_part
        (опционально, потому что это семантически верно: процесс состоит из этапов).
        """
        tpl = self._load_prompt("generate_precedes")
        rows: list[dict] = []
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

        for i, topic in enumerate(topics, 1):
            if verbose:
                print(f"[{i:>3}/{len(topics)}] {topic!r}", end=" ", flush=True)
            try:
                raw = self.provider.complete(tpl.format(topic=topic))
            except Exception as e:
                if verbose:
                    print(f"ERROR: {e}")
                continue
            if self.sleep_between:
                time.sleep(self.sleep_between)
            data = _extract_json(raw) or {}
            if not data.get("is_sequential"):
                if verbose:
                    print("(не последовательный)")
                continue
            stages = [str(s).strip() for s in data.get("stages", []) if str(s).strip()]
            if len(stages) < 2:
                if verbose:
                    print("(мало этапов)")
                continue
            # precedes-пары: соседние этапы
            for a, b in zip(stages[:-1], stages[1:]):
                rows.append({
                    "u_text":  a,
                    "v_text":  b,
                    "relation": "precedes",
                    "source":   "llm",
                    "seed":     topic,
                    "llm_model": self.provider.name,
                    "extracted_ts": ts,
                })
            if verbose:
                print(f"+{len(stages)-1} precedes-пар")

        return pd.DataFrame(rows)


# =============================================================================
# Готовые наборы topics для precedes
# =============================================================================

BIOLOGY_PRECEDES_TOPICS: list[str] = [
    "митоз", "мейоз", "клеточный цикл",
    "фотосинтез", "клеточное дыхание", "гликолиз", "цикл Кребса",
    "транскрипция", "трансляция", "репликация ДНК",
    "эмбриогенез", "оплодотворение", "развитие лягушки",
    "пищеварение у человека", "свёртывание крови",
    "сукцессия экосистемы", "эволюция видов по Дарвину",
    "иммунный ответ", "воспалительная реакция",
]
