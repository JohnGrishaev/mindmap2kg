"""
Сборщик размеченных пар "родитель → потомок" из Wikidata.

Идея:
  Для каждого класса нашей таксономии и каждого его Wikidata-предиката
  (см. mapping в коде ниже) выполняем направленный SPARQL-запрос.
  Каждая возвращённая пара получает relation_id из нашей таксономии,
  сохраняется в data/labeled/annotations.csv с метаданными.

Что НЕ собираем:
  * `precedes` — в Wikidata только 1 биологическая пара (см. probe report);
    собирается через LLM отдельным модулем.
  * `associated_with` — fallback-класс, синтетика не нужна.

Использование:
    from mindmap2kg.annotation.wikidata_extractor import WikidataExtractor
    extr = WikidataExtractor(taxonomy_path="configs/taxonomy.yaml")
    df = extr.extract(seeds=["клетка", "митохондрия", ...])
    df.to_csv("data/labeled/annotations.csv", index=False)
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
import yaml

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Маппинг: relation_id в нашей таксономии → список (Wikidata-property, direction)
#
# direction указывает, какой формирует SPARQL-паттерн:
#   "out": seed-сущность ВЫСТУПАЕТ КАК СУБЪЕКТ предиката, т.е. SPARQL
#          { wd:SEED wdt:PXX ?other }.
#          Это нужно когда: предикат естественно направлен от parent к child
#          в нашей таксономии (P527 has_part: целое → часть).
#   "in":  seed-сущность ВЫСТУПАЕТ КАК ОБЪЕКТ предиката, т.е. SPARQL
#          { ?other wdt:PXX wd:SEED }.
#          Это нужно когда: предикат естественно направлен child → parent
#          (P279 subclass_of: подкласс → надкласс), и мы инвертируем.
#
# В обоих случаях после извлечения пара формируется как (seed_text, other_text),
# то есть seed всегда — родитель в нашей таксономии.
# -----------------------------------------------------------------------------
TAXONOMY_MAPPING: dict[str, list[tuple[str, str, str]]] = {
    "has_part":      [("P527",  "has part",      "out")],
    "has_example":   [("P279",  "subclass of",   "in"),
                      ("P31",   "instance of",   "in")],
    "has_property":  [("P1552", "has quality",   "out")],
    "has_function":  [("P366",  "has use",       "out"),
                      ("P1535", "used by",       "out")],
    "causes":        [("P1542", "has effect",    "out"),
                      ("P828",  "has cause",     "in")],
    # precedes — собирается LLM-ом
    # associated_with — fallback, не собираем
}


@dataclass
class ExtractorConfig:
    sparql_endpoint: str = "https://query.wikidata.org/sparql"
    wb_api: str = "https://www.wikidata.org/w/api.php"
    user_agent: str = "mindmap2kg-research/0.1 (academic data collection)"
    sparql_sleep: float = 0.4
    wb_sleep: float = 0.7
    per_query_limit: int = 500


class WikidataExtractor:
    def __init__(self, taxonomy_path: str | Path,
                 config: ExtractorConfig | None = None):
        self.taxonomy = yaml.safe_load(
            Path(taxonomy_path).read_text(encoding="utf-8"))
        self.taxonomy_version = self.taxonomy.get("version", "unknown")
        self.cfg = config or ExtractorConfig()
        # Кэш меток QID → русская метка
        self._label_cache: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Низкоуровневые HTTP-вызовы
    # ------------------------------------------------------------------

    def _sparql(self, query: str, retries: int = 3) -> list[dict] | None:
        headers = {"Accept": "application/sparql-results+json",
                   "User-Agent": self.cfg.user_agent}
        for attempt in range(retries):
            try:
                r = requests.get(self.cfg.sparql_endpoint,
                                 params={"query": query},
                                 headers=headers, timeout=60)
                if r.status_code == 200:
                    time.sleep(self.cfg.sparql_sleep)
                    return r.json()["results"]["bindings"]
                if r.status_code in (429, 502, 503, 504):
                    wait = 2 ** attempt
                    logger.warning("HTTP %s, retrying in %ss", r.status_code, wait)
                    time.sleep(wait)
                    continue
                logger.error("SPARQL HTTP %s: %s", r.status_code, r.text[:200])
                return None
            except requests.RequestException as e:
                logger.warning("Network error: %s", e)
                time.sleep(2 ** attempt)
        return None

    def _find_qid(self, label: str) -> str | None:
        for attempt in range(3):
            try:
                r = requests.get(self.cfg.wb_api,
                                 headers={"User-Agent": self.cfg.user_agent},
                                 timeout=10,
                                 params={
                                     "action": "wbsearchentities",
                                     "search": label,
                                     "language": "ru",
                                     "format": "json",
                                     "limit": 1,
                                 })
                time.sleep(self.cfg.wb_sleep)
                if r.status_code == 429:
                    time.sleep(2 ** (attempt + 1))
                    continue
                if r.status_code != 200:
                    return None
                hits = r.json().get("search", [])
                return hits[0]["id"] if hits else None
            except Exception as e:
                logger.warning("wbsearchentities('%s'): %s", label, e)
                return None
        return None

    def _get_label_ru(self, qid: str) -> str | None:
        """Получить русскую метку для QID (с кэшированием)."""
        if qid in self._label_cache:
            return self._label_cache[qid]
        q = f"""
        SELECT ?label WHERE {{
          wd:{qid} rdfs:label ?label .
          FILTER(LANG(?label) = "ru")
        }} LIMIT 1
        """
        rows = self._sparql(q)
        if not rows:
            return None
        label = rows[0]["label"]["value"]
        self._label_cache[qid] = label
        return label

    # ------------------------------------------------------------------
    # Основная логика извлечения
    # ------------------------------------------------------------------

    def _fetch_pairs(self, seed_qid: str, seed_text: str,
                     predicate: str, direction: str) -> list[tuple[str, str]]:
        """
        Возвращает список пар (parent_text, child_text) в нашей таксономии,
        где seed выступает родителем.
        """
        if direction == "out":
            triple = f"wd:{seed_qid} wdt:{predicate} ?other"
        else:  # "in"
            triple = f"?other wdt:{predicate} wd:{seed_qid}"

        q = f"""
        SELECT ?other ?otherLabel WHERE {{
          {triple} .
          ?other rdfs:label ?otherLabel .
          FILTER(LANG(?otherLabel) = "ru")
        }} LIMIT {self.cfg.per_query_limit}
        """
        rows = self._sparql(q)
        if not rows:
            return []
        return [(seed_text, r["otherLabel"]["value"]) for r in rows]

    def extract(self, seeds: list[str],
                verbose: bool = True) -> pd.DataFrame:
        """Главная точка входа. Возвращает DataFrame с разметкой."""
        rows: list[dict] = []
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

        for i, seed in enumerate(seeds, 1):
            if verbose:
                print(f"[{i:>3}/{len(seeds)}] {seed!r}", end=" ", flush=True)

            qid = self._find_qid(seed)
            if not qid:
                if verbose: print("(QID не найден)")
                continue
            seed_label = self._get_label_ru(qid) or seed

            per_seed = 0
            for rel_id, predicates in TAXONOMY_MAPPING.items():
                for pid, _, direction in predicates:
                    pairs = self._fetch_pairs(qid, seed_label, pid, direction)
                    for parent_text, child_text in pairs:
                        # пропускаем самосвязи и пустые
                        if not child_text or parent_text == child_text:
                            continue
                        rows.append({
                            "u_text": parent_text,
                            "v_text": child_text,
                            "relation": rel_id,
                            "source": "wikidata",
                            "wikidata_predicate": pid,
                            "wikidata_direction": direction,
                            "seed": seed,
                            "seed_qid": qid,
                            "taxonomy_version": self.taxonomy_version,
                            "extracted_ts": ts,
                        })
                        per_seed += 1
            if verbose:
                print(f"QID={qid}  +{per_seed} пар")

        df = pd.DataFrame(rows)
        if df.empty:
            return df

        # Дедупликация: одна и та же пара с одним и тем же relation —
        # достаточно одного экземпляра, даже если её нашли через разные seed.
        before = len(df)
        df = df.drop_duplicates(subset=["u_text", "v_text", "relation"], keep="first")
        if verbose:
            print(f"\nДедуплицировано: {before} → {len(df)} пар")

        return df.reset_index(drop=True)


# -----------------------------------------------------------------------------
# Seed-списки.
#
# BIOLOGY_SEEDS_DEFAULT — базовый список (тот же, что в probe v2).
# Дал жёсткий перекос: has_example=91%, миноры по 15-55 пар.
#
# BIOLOGY_SEEDS_TARGETED — расширение под минорные классы:
#   - инфекционные агенты и заболевания → causes (P1542 has effect)
#   - ферменты и гормоны → has_function (P366 has use)
#   - физико-химические сущности → has_property (P1552 has quality)
#
# Используй extract(seeds=BIOLOGY_SEEDS_DEFAULT + BIOLOGY_SEEDS_TARGETED) для
# полного покрытия. Дедупликация снимет пересечения.
# -----------------------------------------------------------------------------
BIOLOGY_SEEDS_DEFAULT: list[str] = [
    "клетка", "ядро клетки", "митохондрия", "рибосома", "клеточная мембрана", "хлоропласт",
    "сердце", "лёгкое", "головной мозг", "печень", "кровь", "скелет",
    "растение", "корень", "стебель", "лист", "цветок", "фотосинтез",
    "млекопитающие", "птицы", "рыбы", "насекомые", "позвоночные",
    "фермент", "белок", "ДНК", "мутация", "митоз", "эволюция",
    "экосистема", "вид", "популяция",
]

BIOLOGY_SEEDS_TARGETED: list[str] = [
    # --- под causes (инфекционные агенты, токсины, заболевания) ---
    "вирус", "бактерия", "грибок", "паразит", "прион", "вирус гриппа",
    "ВИЧ", "коронавирус", "бактерия туберкулёза", "холерный вибрион",
    "канцероген", "тератоген", "мутаген", "токсин", "аллерген",
    "ультрафиолетовое излучение", "ионизирующее излучение",
    "диабет", "гипертония", "атеросклероз", "инфаркт миокарда",

    # --- под has_function (ферменты, гормоны, органеллы с функцией) ---
    "ДНК-полимераза", "РНК-полимераза", "рибонуклеаза", "амилаза",
    "пепсин", "трипсин", "гемоглобин", "инсулин", "адреналин", "тестостерон",
    "эстроген", "тироксин", "антитело", "иммуноглобулин",
    "хлорофилл", "АТФ-синтаза", "цитохром",

    # --- под has_property (вещества/процессы с измеримыми свойствами) ---
    "вода", "глюкоза", "липид", "аминокислота", "холестерин",
    "крахмал", "целлюлоза", "коллаген", "кератин",
    "осмос", "диффузия", "ферментация", "дыхание",
]

BIOLOGY_SEEDS_FULL: list[str] = BIOLOGY_SEEDS_DEFAULT + BIOLOGY_SEEDS_TARGETED
