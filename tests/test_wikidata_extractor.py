"""
Тест экстрактора с моками SPARQL/wbsearchentities.
Без сети, проверяем только логику сборки пар и направление.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd

import mindmap2kg  # noqa: F401
from mindmap2kg.annotation.wikidata_extractor import WikidataExtractor


def _mk_sparql_response(items: list[tuple[str, str]]):
    """Превращает [(other_qid, other_label), ...] в формат ответа SPARQL."""
    return [
        {"other":      {"value": f"http://www.wikidata.org/entity/{q}"},
         "otherLabel": {"value": label}}
        for q, label in items
    ]


def _mk_label_response(label: str):
    return [{"label": {"value": label}}]


def test_extractor_directions_and_dedup(tmp_path: Path):
    """Главный тест: имитируем ответы SPARQL и проверяем, что:
       1) направление пар корректное (seed всегда родитель)
       2) дедупликация работает
       3) разные предикаты под одним relation_id корректно собираются
    """

    taxonomy_path = Path(__file__).parent.parent / "configs" / "taxonomy.yaml"
    extractor = WikidataExtractor(taxonomy_path=str(taxonomy_path))

    # Имитируем ответы wbsearchentities и SPARQL
    def fake_find_qid(self, label):
        return {"клетка": "Q7868", "митохондрия": "Q39572"}.get(label)

    def fake_sparql(self, query, retries=3):
        # Запрос метки QID
        if "rdfs:label ?label" in query and "LIMIT 1" in query:
            if "Q7868" in query:  return _mk_label_response("клетка")
            if "Q39572" in query: return _mk_label_response("митохондрия")
            return []
        # Запрос пар: P527 has_part из митохондрии
        if "wd:Q39572 wdt:P527" in query:
            return _mk_sparql_response([
                ("Q11", "Кристы"),
                ("Q12", "Митохондриальная ДНК"),
                ("Q13", "Матрикс"),
            ])
        # P279 incoming для клетки: ?other subclass_of клетка → клетка has_example ?other
        if "?other wdt:P279 wd:Q7868" in query:
            return _mk_sparql_response([
                ("Q21", "нейрон"),
                ("Q22", "кардиомиоцит"),
                ("Q21", "нейрон"),  # дубликат — должен схлопнуться при dedup
            ])
        # Все остальные предикаты — пусто
        return []

    with patch.object(WikidataExtractor, "_find_qid", fake_find_qid), \
         patch.object(WikidataExtractor, "_sparql", fake_sparql):
        df = extractor.extract(["клетка", "митохондрия"], verbose=False)

    # 1) Направление: клетка → нейрон (не наоборот)
    has_example_pairs = df[df["relation"] == "has_example"]
    assert len(has_example_pairs) == 2  # после dedup
    assert set(has_example_pairs["u_text"]) == {"клетка"}
    assert set(has_example_pairs["v_text"]) == {"нейрон", "кардиомиоцит"}

    # 2) has_part: митохондрия → её части
    has_part_pairs = df[df["relation"] == "has_part"]
    assert len(has_part_pairs) == 3
    assert set(has_part_pairs["u_text"]) == {"митохондрия"}
    assert set(has_part_pairs["v_text"]) == {"Кристы", "Митохондриальная ДНК", "Матрикс"}

    # 3) Метаданные на месте
    assert (df["source"] == "wikidata").all()
    assert (df["taxonomy_version"] == "0.1").all()
    assert "wikidata_predicate" in df.columns
    assert "seed_qid" in df.columns

    print(f"✓ Тест прошёл: {len(df)} пар извлечено")
    print(df[["u_text", "v_text", "relation", "wikidata_predicate"]].to_string())


def test_missing_qid_skipped():
    """Seed без QID не должен ломать прогон."""
    taxonomy_path = Path(__file__).parent.parent / "configs" / "taxonomy.yaml"
    extractor = WikidataExtractor(taxonomy_path=str(taxonomy_path))

    with patch.object(WikidataExtractor, "_find_qid", lambda self, l: None):
        df = extractor.extract(["несуществующий_термин"], verbose=False)

    assert df.empty
    print("✓ Несуществующие seed-термины корректно пропускаются")


if __name__ == "__main__":
    tmp = Path("/tmp")
    test_extractor_directions_and_dedup(tmp)
    test_missing_qid_skipped()
    print("\n✓ Все тесты прошли")
