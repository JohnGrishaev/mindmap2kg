"""
CLI для LLM-разметки.

Два режима:

  validate — пройти по существующим аннотациям и проставить llm_verdict.
             По умолчанию валидируется только has_property и has_function
             (классы с шумной семантикой в Wikidata).

      python scripts/llm_annotate.py validate \\
          --annotations data/labeled/annotations.csv \\
          --output data/labeled/annotations_validated.csv \\
          --model gpt-4o-mini \\
          --limit 200

  precedes — собрать пары precedes из списка процессов.

      python scripts/llm_annotate.py precedes \\
          --output data/labeled/precedes_pairs.csv \\
          --model gpt-4o-mini

Переменные окружения для OpenAI-совместимого API:
  LLM_API_KEY      — обязательно
  LLM_BASE_URL     — опционально (для vLLM / LM Studio / Ollama)
  LLM_MODEL        — опционально (можно переопределить --model)

Для теста без сети:
  python scripts/llm_annotate.py precedes --output /tmp/p.csv --mock
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

import mindmap2kg  # noqa: F401
from mindmap2kg.annotation.llm_annotator import (
    BIOLOGY_PRECEDES_TOPICS,
    LLMAnnotator,
    MockProvider,
    OpenAICompatibleProvider,
)


def _make_provider(args):
    if args.mock:
        return MockProvider()
    return OpenAICompatibleProvider(
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
    )


def cmd_validate(args) -> int:
    df = pd.read_csv(args.annotations)
    print(f"Загружено пар: {len(df)}")

    only = None
    if args.only_relations:
        only = [s.strip() for s in args.only_relations.split(",") if s.strip()]
        print(f"Валидируем только: {only}")

    annot = LLMAnnotator(provider=_make_provider(args),
                         sleep_between=args.sleep)
    out = annot.validate_pairs(df,
                               only_relations=only,
                               limit=args.limit,
                               verbose=not args.quiet)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False, encoding="utf-8")

    # сводка по вердиктам
    if "llm_verdict" in out.columns:
        sub = out[out["llm_verdict"] != ""]
        print(f"\nВалидировано: {len(sub)}")
        print(sub["llm_verdict"].value_counts().to_string())
        wrong = sub[sub["llm_verdict"] == "wrong"]
        if len(wrong):
            print(f"\nИсправлений по классам предложено:")
            print(wrong["llm_suggested"].value_counts().to_string())
    print(f"\nСохранено: {args.output}")
    return 0


def cmd_precedes(args) -> int:
    if args.topics_file:
        topics = [s.strip() for s in
                  Path(args.topics_file).read_text(encoding="utf-8").splitlines()
                  if s.strip() and not s.startswith("#")]
    else:
        topics = BIOLOGY_PRECEDES_TOPICS
    print(f"Topics: {len(topics)}")

    annot = LLMAnnotator(provider=_make_provider(args),
                         sleep_between=args.sleep)
    out = annot.generate_precedes(topics, verbose=not args.quiet)
    if out.empty:
        print("Не извлечено ни одной пары")
        return 1
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False, encoding="utf-8")
    print(f"\nСобрано precedes-пар: {len(out)}")
    print(f"Сохранено: {args.output}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model", default=None,
                    help="Имя модели (или env LLM_MODEL)")
    ap.add_argument("--base-url", default=None,
                    help="OpenAI-совместимый endpoint (или env LLM_BASE_URL)")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--sleep", type=float, default=0.0,
                    help="Пауза между запросами, сек (для rate limit)")
    ap.add_argument("--mock", action="store_true",
                    help="Использовать MockProvider (для smoke-тестов)")
    ap.add_argument("--quiet", action="store_true")

    sub = ap.add_subparsers(dest="cmd", required=True)

    # validate
    p1 = sub.add_parser("validate", help="Валидировать существующие пары")
    p1.add_argument("--annotations", required=True)
    p1.add_argument("--output", required=True)
    p1.add_argument("--only-relations", default="has_property,has_function",
                    help="Через запятую, какие relation валидировать "
                         "(default: шумные классы). Пусто = все.")
    p1.add_argument("--limit", type=int, default=None,
                    help="Максимум пар (для пилота)")

    # precedes
    p2 = sub.add_parser("precedes", help="Сгенерировать precedes-пары")
    p2.add_argument("--output", required=True)
    p2.add_argument("--topics-file", default=None,
                    help="Файл с topics (по одному на строку)")

    args = ap.parse_args()
    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if args.cmd == "validate":
        return cmd_validate(args)
    if args.cmd == "precedes":
        return cmd_precedes(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
