"""
Обёртка sklearn-классификаторов под наш контракт BaseClassifier.

Поддерживает:
  * gbm — GradientBoostingClassifier (стабильный, без зависимостей)
  * logreg — LogisticRegression (быстрый бейзлайн)
  * rf — RandomForestClassifier
  * hgbm — HistGradientBoostingClassifier (быстрее на больших данных)
  * tfidf_logreg — логистическая регрессия на символьных n-граммах меток
    u_text и v_text (TF-IDF, 2–5 символов) плюс числовые признаки.
    n-граммы ловят морфологию меток (-ость, -ние, -аза, -оз …), которую не
    видят длины и коэффициенты Жаккара. Если среди признаков есть полные
    SBERT-векторы (sbert_u_*, sbert_v_*, sbert_diff_*, sbert_hadamard_*), они
    идут отдельным блоком: стандартизуются и делятся на sqrt(размерность),
    чтобы 1536 плотных признаков не заглушали n-граммы (без этого
    macro-F1 0.435, с ним 0.502 на 20 групповых разбиениях).

Модель ОБУЧАЕТСЯ внешним скриптом (scripts/train_classifier.py) и сохраняется
joblib-ом в models/{run_id}.joblib. Здесь предусмотрены два режима:
  * predict() — модель уже загружена (через load() или fit() в скрипте)
  * load(path) — подгрузить обученную модель и встретить пайплайн

В пайплайне (configs/*.yaml) указываем classifier:
    name: sklearn
    options:
      backend: tfidf_logreg
      model_path: models/exp_tfidf.joblib
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

# Бэкенды, которые помимо числовых признаков читают сырые тексты меток
TEXT_BACKENDS = {"tfidf_logreg"}
TEXT_COLS = ["u_text", "v_text"]
SBERT_VECTOR_PREFIXES = ("sbert_u_", "sbert_v_", "sbert_diff_", "sbert_hadamard_")


from sklearn.base import BaseEstimator, TransformerMixin  # noqa: E402


class BlockWeight(TransformerMixin, BaseEstimator):
    """Умножает блок признаков на weight / sqrt(число признаков блока).

    Нужен, чтобы вклад блока в норму вектора (и в штраф L2) не зависел от
    его размерности. Класс модульного уровня — иначе joblib не сохранит модель.
    """

    def __init__(self, weight: float = 1.0):
        self.weight = weight

    def fit(self, X, y=None):
        self.scale_ = self.weight / np.sqrt(max(1, X.shape[1]))
        return self

    def transform(self, X):
        return X * self.scale_
BACKENDS = ["gbm", "hgbm", "rf", "logreg", "tfidf_logreg"]


# Каркасные конструкторы. Импорт sklearn — ленивый.
def _make_estimator(backend: str, feature_columns: list[str] | None = None, **kw) -> Any:
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
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        kw.setdefault("max_iter", 2000)
        kw.setdefault("class_weight", "balanced")
        # Признаки разного масштаба (длины, Жаккар, косинус) — без
        # стандартизации логистическая регрессия сходится плохо.
        return make_pipeline(StandardScaler(), LogisticRegression(**kw))
    if backend == "tfidf_logreg":
        from sklearn.compose import ColumnTransformer
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        kw.pop("random_state", None)
        kw.setdefault("C", 2.0)
        kw.setdefault("max_iter", 5000)
        kw.setdefault("class_weight", "balanced")

        def tfidf():
            return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5),
                                   lowercase=True, sublinear_tf=True, min_df=2)

        from sklearn.pipeline import make_pipeline
        cols = list(feature_columns or [])
        vec_cols = [c for c in cols if c.startswith(SBERT_VECTOR_PREFIXES)]
        num_cols = [c for c in cols if c not in vec_cols]
        sbert_weight = kw.pop("sbert_weight", 1.0)
        transformers = [("u", tfidf(), "u_text"), ("v", tfidf(), "v_text")]
        if num_cols:
            transformers.append(("num", StandardScaler(), num_cols))
        if vec_cols:
            transformers.append(("sbert_vec", make_pipeline(
                StandardScaler(), BlockWeight(sbert_weight)), vec_cols))
        return Pipeline([("features", ColumnTransformer(transformers)),
                         ("clf", LogisticRegression(**kw))])
    raise ValueError(f"Unknown backend: {backend}")


def make_input(df: pd.DataFrame, backend: str, feature_columns: list[str]):
    """Матрица входа для estimator: numpy для числовых бэкендов,
    DataFrame с текстами меток для текстовых."""
    if backend in TEXT_BACKENDS:
        X = df[feature_columns].astype(float).fillna(0)
        for c in TEXT_COLS:
            X[c] = df[c].astype(str).str.strip().values
        return X
    return df[feature_columns].astype(float).fillna(0).values


def fit_estimator(est: Any, X, y, backend: str, sample_weight=None) -> Any:
    """fit с передачей sample_weight в нужный шаг (для Pipeline)."""
    if sample_weight is None:
        return est.fit(X, y)
    if backend in {"gbm", "hgbm"}:
        return est.fit(X, y, sample_weight=sample_weight)
    if backend == "tfidf_logreg":
        return est.fit(X, y, clf__sample_weight=sample_weight)
    return est.fit(X, y)


# Колонки, которые НЕ являются признаками (идентификаторы, тексты)
NON_FEATURE_COLS = {
    "pair_id", "u_id", "v_id", "u_text", "v_text",
    "relation", "source", "seed", "seed_qid", "extracted_ts",
    "wikidata_predicate", "wikidata_direction", "taxonomy_version",
    "curated_version",
}

# Признаками считаются ТОЛЬКО колонки, созданные экстракторами признаков.
# Раньше брались все числовые колонки, кроме NON_FEATURE_COLS, и в признаки
# попадала служебная колонка curated_version (0.1 у всех пар precedes, NaN у
# остальных) — прямая утечка метки класса precedes.
FEATURE_PREFIXES = ("lex_", "sbert_", "topo_")


def select_feature_columns(df: pd.DataFrame) -> list[str]:
    """Отбирает числовые/bool колонки, созданные экстракторами признаков."""
    cols = []
    for c in df.columns:
        if c in NON_FEATURE_COLS or not c.startswith(FEATURE_PREFIXES):
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
        if model_path:
            if not Path(model_path).exists():
                raise FileNotFoundError(
                    f"Файл модели не найден: {model_path}. "
                    "Запусти scripts/train_classifier.py.")
            self.load(model_path)

    # ---- fit / save / load --------------------------------------------------

    def fit(self, X: pd.DataFrame, y: pd.Series,
            feature_columns: list[str] | None = None,
            sample_weight=None) -> "SklearnClassifier":
        self.feature_columns = feature_columns or select_feature_columns(X)
        if not self.feature_columns and self.backend not in TEXT_BACKENDS:
            raise ValueError("Не нашёл числовых признаков в DataFrame")
        self.estimator = _make_estimator(self.backend, self.feature_columns,
                                         **self.estimator_kwargs)
        Xn = make_input(X, self.backend, self.feature_columns)
        fit_estimator(self.estimator, Xn, y.values, self.backend, sample_weight)
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
                "SklearnClassifier не обучен и model_path не задан. "
                "Запусти scripts/train_classifier.py.")
        missing = [c for c in self.feature_columns if c not in df.columns]
        if missing:
            raise ValueError(
                f"Модель обучена на признаках, которых нет во входных данных: "
                f"{missing}. Проверь список features в конфигурации пайплайна.")
        X = make_input(df, self.backend, self.feature_columns)
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
