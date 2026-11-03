"""
Обёртка sklearn-классификаторов под наш контракт BaseClassifier.

Поддерживает:
  * gbm — GradientBoostingClassifier (стабильный, без зависимостей)
  * logreg — LogisticRegression (быстрый бейзлайн)
  * rf — RandomForestClassifier
  * hgbm — HistGradientBoostingClassifier (быстрее на больших данных)

Модель ОБУЧАЕТСЯ внешним скриптом (scripts/train_classifier.py) и сохраняется
joblib-ом в models/{run_id}.joblib. Здесь предусмотрены два режима:
  * predict() — модель уже загружена (через load() или fit() в скрипте)
  * load(path) — подгрузить обученную модель и встретить пайплайн

В пайплайне (configs/*.yaml) указываем classifier:
    name: sklearn
    options:
      backend: gbm
      model_path: models/exp_baseline.joblib
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ..core.base import BaseClassifier
from ..core.registry import register
from ..core.schemas import Prediction

logger = logging.getLogger(__name__)


# Каркасные конструкторы. Импорт sklearn — ленивый.
def _make_estimator(backend: str, **kw) -> Any:
    if backend == "gbm":
        from sklearn.ensemble import GradientBoostingClassifier
        return GradientBoostingClassifier(**kw)
    if backend == "hgbm":
        from sklearn.ensemble import HistGradientBoostingClassifier
        return HistGradientBoostingClassifier(**kw)
    if backend == "rf":
        from sklearn.ensemble import RandomForestClassifier
        kw.setdefault("n_estimators", 300)
        kw.setdefault("class_weight", "balanced")
        return RandomForestClassifier(**kw)
    if backend == "logreg":
        from sklearn.linear_model import LogisticRegression
        kw.setdefault("max_iter", 2000)
        kw.setdefault("class_weight", "balanced")
        return LogisticRegression(**kw)
    raise ValueError(f"Unknown backend: {backend}")


# Колонки, которые НЕ являются признаками (идентификаторы, тексты)
NON_FEATURE_COLS = {
    "pair_id", "u_id", "v_id", "u_text", "v_text",
    "relation", "source", "seed", "seed_qid", "extracted_ts",
    "wikidata_predicate", "wikidata_direction", "taxonomy_version",
}


def select_feature_columns(df: pd.DataFrame) -> list[str]:
    """Отбирает числовые/bool колонки, исключая идентификаторы и метки."""
    cols = []
    for c in df.columns:
        if c in NON_FEATURE_COLS:
            continue
        if pd.api.types.is_numeric_dtype(df[c]) or pd.api.types.is_bool_dtype(df[c]):
            cols.append(c)
    return cols


@register("classifier", "sklearn")
class SklearnClassifier(BaseClassifier):
    def __init__(self, taxonomy: dict,
                 backend: str = "gbm",
                 model_path: str | None = None,
                 **estimator_kwargs):
        self.classes = [r["id"] for r in taxonomy["relations"]]
        self.backend = backend
        self.estimator_kwargs = estimator_kwargs
        self.estimator: Any = None
        self.feature_columns: list[str] | None = None
        if model_path and Path(model_path).exists():
            self.load(model_path)

    # ---- fit / save / load --------------------------------------------------

    def fit(self, X: pd.DataFrame, y: pd.Series,
            feature_columns: list[str] | None = None) -> "SklearnClassifier":
        self.feature_columns = feature_columns or select_feature_columns(X)
        if not self.feature_columns:
            raise ValueError("Не нашёл числовых признаков в DataFrame")
        self.estimator = _make_estimator(self.backend, **self.estimator_kwargs)
        Xn = X[self.feature_columns].astype(float).values
        self.estimator.fit(Xn, y.values)
        logger.info("Обучен %s: %d признаков, %d классов",
                    self.backend, len(self.feature_columns),
                    len(self.estimator.classes_))
        return self

    def save(self, path: str | Path) -> None:
        import joblib
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "estimator": self.estimator,
            "feature_columns": self.feature_columns,
            "backend": self.backend,
            "classes": list(self.estimator.classes_) if self.estimator else [],
        }, path)
        logger.info("Сохранено: %s", path)

    def load(self, path: str | Path) -> "SklearnClassifier":
        import joblib
        d = joblib.load(path)
        self.estimator = d["estimator"]
        self.feature_columns = d["feature_columns"]
        self.backend = d.get("backend", self.backend)
        return self

    # ---- predict ------------------------------------------------------------

    def predict(self, df: pd.DataFrame) -> list[Prediction]:
        if self.estimator is None:
            raise RuntimeError(
                "SklearnClassifier не обучен и model_path не задан/не существует. "
                "Запусти scripts/train_classifier.py.")
        X = df[self.feature_columns].astype(float).values
        proba = self.estimator.predict_proba(X)
        classes = list(self.estimator.classes_)

        preds: list[Prediction] = []
        for i, row in enumerate(df.itertuples(index=False)):
            scores = {c: float(p) for c, p in zip(classes, proba[i])}
            winner_idx = int(np.argmax(proba[i]))
            winner = classes[winner_idx]
            preds.append(Prediction(
                pair_id=getattr(row, "pair_id"),
                relation=winner,
                confidence=float(proba[i][winner_idx]),
                all_scores=scores,
            ))
        return preds
