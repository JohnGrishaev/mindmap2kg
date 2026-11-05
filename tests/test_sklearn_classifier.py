"""Smoke-тесты sklearn-обёртки (без SBERT, на синтетических числовых признаках)."""
import pandas as pd
import pytest

pytest.importorskip("sklearn")

import yaml
from pathlib import Path

import mindmap2kg  # noqa: F401  — регистрирует плагины
from mindmap2kg.classifiers.sklearn_wrapper import (
    SklearnClassifier, select_feature_columns,
)


def _taxonomy():
    p = Path(__file__).resolve().parents[1] / "configs" / "taxonomy.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def test_select_feature_columns_skips_ids():
    df = pd.DataFrame({
        "pair_id": ["p1", "p2"],
        "u_text": ["a", "b"],
        "v_text": ["c", "d"],
        "relation": ["has_part", "has_example"],
        "lex_x1": [1.0, 2.0],
        "topo_x2": [True, False],
    })
    cols = select_feature_columns(df)
    assert cols == ["lex_x1", "topo_x2"]


def test_select_feature_columns_skips_metadata_leak():
    """curated_version есть только у пар precedes — это не признак."""
    df = pd.DataFrame({
        "relation": ["precedes", "has_part"],
        "curated_version": [0.1, None],
        "taxonomy_version": [0.1, 0.1],
        "lex_len_u": [5, 7],
    })
    assert select_feature_columns(df) == ["lex_len_u"]


def test_fit_predict_save_load(tmp_path):
    import numpy as np
    rng = np.random.RandomState(0)
    n = 80
    df = pd.DataFrame({
        "pair_id": [f"p{i}" for i in range(n)],
        "lex_x1": rng.randn(n),
        "lex_x2": rng.randn(n),
        "relation": ["has_part" if x > 0 else "has_example"
                     for x in rng.randn(n)],
    })

    tax = _taxonomy()
    clf = SklearnClassifier(taxonomy=tax, backend="logreg")
    clf.fit(df, df["relation"])
    preds = clf.predict(df)
    assert len(preds) == n
    assert all(p.relation in {"has_part", "has_example"} for p in preds)

    # сохранение / загрузка
    path = tmp_path / "m.joblib"
    clf.save(path)

    clf2 = SklearnClassifier(taxonomy=tax, backend="logreg", model_path=str(path))
    preds2 = clf2.predict(df)
    assert [p.relation for p in preds] == [p.relation for p in preds2]


def test_tfidf_logreg_uses_label_text(tmp_path):
    """tfidf_logreg учится по тексту меток: суффикс -ость → has_property."""
    props = ["прозрачность", "твёрдость", "вязкость", "плотность", "упругость",
             "прочность", "текучесть", "летучесть", "хрупкость", "мягкость"]
    parts = ["корень", "стебель", "лист", "ядро", "рибосома",
             "мембрана", "цветок", "плод", "семя", "почка"]
    df = pd.DataFrame({
        "pair_id": [f"p{i}" for i in range(20)],
        "u_text": ["объект"] * 20,
        "v_text": props + parts,
        "lex_len_v": [len(t) for t in props + parts],
        "relation": ["has_property"] * 10 + ["has_part"] * 10,
    })
    clf = SklearnClassifier(taxonomy=_taxonomy(), backend="tfidf_logreg")
    clf.fit(df, df["relation"])
    test = pd.DataFrame({"pair_id": ["t1", "t2"], "u_text": ["вода", "растение"],
                         "v_text": ["солёность", "лист"], "lex_len_v": [9, 4]})
    assert [p.relation for p in clf.predict(test)] == ["has_property", "has_part"]

    path = tmp_path / "m.joblib"
    clf.save(path)
    clf2 = SklearnClassifier(taxonomy=_taxonomy(), backend="tfidf_logreg", model_path=str(path))
    assert [p.relation for p in clf2.predict(test)] == ["has_property", "has_part"]


def test_predict_reports_missing_features():
    import numpy as np
    df = pd.DataFrame({"pair_id": ["a", "b", "c", "d"], "lex_a": np.arange(4.0),
                       "relation": ["has_part", "has_example"] * 2})
    clf = SklearnClassifier(taxonomy=_taxonomy(), backend="logreg").fit(df, df["relation"])
    with pytest.raises(ValueError, match="lex_a"):
        clf.predict(pd.DataFrame({"pair_id": ["x"]}))
