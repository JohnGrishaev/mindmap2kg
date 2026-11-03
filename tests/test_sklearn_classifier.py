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
        "x1": [1.0, 2.0],
        "x2": [True, False],
    })
    cols = select_feature_columns(df)
    assert cols == ["x1", "x2"]


def test_fit_predict_save_load(tmp_path):
    import numpy as np
    rng = np.random.RandomState(0)
    n = 80
    df = pd.DataFrame({
        "pair_id": [f"p{i}" for i in range(n)],
        "x1": rng.randn(n),
        "x2": rng.randn(n),
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
