"""
SBERT-эмбеддинги текстов узлов + производные численные признаки.

Модель по умолчанию — sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
(384-мерные эмбеддинги, RU/EN из коробки, ~120 MB).
Альтернативы: cointegrated/rubert-tiny2 (быстрее, 312 dim, RU-only).

Что добавляет в DataFrame:
  * sbert_cos       — косинусная близость u и v
  * sbert_l2        — евклидово расстояние
  * sbert_dot       — скалярное произведение (на нормализованных векторах = cos)
  * sbert_u_*       — компоненты вектора u (опционально, флаг include_vectors)
  * sbert_v_*       — компоненты вектора v
  * sbert_diff_*    — поэлементная разность u - v
  * sbert_hadamard_* — поэлементное произведение u * v

По умолчанию include_vectors=False: для GBM на лексических+топо+скалярных
SBERT-признаках уже достаточно сигнала, а полные векторы (384*4 = 1536 колонок)
раздувают таблицу. Для MLP/нейросети — включить.

Кэш эмбеддингов: словарь text → np.ndarray, лежит на диске рядом с моделью.
Это критично — мы вызываем фичер на каждом запуске пайплайна.
"""
from __future__ import annotations

import hashlib
import logging
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ...core.base import BaseFeature
from ...core.registry import register
from ...core.schemas import MindMap

logger = logging.getLogger(__name__)


@register("feature", "sbert")
class SBertFeatures(BaseFeature):
    def __init__(self,
                 model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                 cache_dir: str = "data/cache/sbert",
                 include_vectors: bool = False,
                 batch_size: int = 64,
                 normalize: bool = True):
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.include_vectors = include_vectors
        self.batch_size = batch_size
        self.normalize = normalize
        self._model: Any = None
        self._cache: dict[str, np.ndarray] = self._load_cache()

    # ---- lazy load и кэш ---------------------------------------------------

    def _model_key(self) -> str:
        return hashlib.md5(self.model_name.encode()).hexdigest()[:12]

    def _cache_path(self) -> Path:
        return self.cache_dir / f"{self._model_key()}.pkl"

    def _load_cache(self) -> dict[str, np.ndarray]:
        p = self._cache_path()
        if p.exists():
            try:
                with p.open("rb") as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning("Кэш SBERT повреждён, начинаю заново: %s", e)
        return {}

    def _save_cache(self) -> None:
        with self._cache_path().open("wb") as f:
            pickle.dump(self._cache, f)

    def _ensure_model(self) -> None:
        if self._model is not None:
            return
        # импорт ленивый: sentence-transformers — тяжёлая зависимость
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "Установи extras: pip install 'mindmap2kg[text]' "
                "(подтянет sentence-transformers)."
            ) from e
        logger.info("Загружаю SBERT-модель %s...", self.model_name)
        self._model = SentenceTransformer(self.model_name)

    # ---- основная логика ---------------------------------------------------

    def _embed(self, texts: list[str]) -> np.ndarray:
        """Возвращает матрицу эмбеддингов (len(texts), dim). С кэшем."""
        # Что нужно реально вычислить
        missing = [t for t in texts if t not in self._cache]
        if missing:
            self._ensure_model()
            unique_missing = list(dict.fromkeys(missing))  # сохраняем порядок, без дублей
            vecs = self._model.encode(
                unique_missing,
                batch_size=self.batch_size,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            for t, v in zip(unique_missing, vecs):
                self._cache[t] = v.astype(np.float32)
            self._save_cache()
        return np.vstack([self._cache[t] for t in texts])

    def transform(self, df: pd.DataFrame, mm: MindMap) -> pd.DataFrame:
        df = df.copy()
        u_vecs = self._embed(df["u_text"].astype(str).tolist())
        v_vecs = self._embed(df["v_text"].astype(str).tolist())

        # Скаляры
        if self.normalize:
            df["sbert_cos"] = (u_vecs * v_vecs).sum(axis=1)
            df["sbert_dot"] = df["sbert_cos"]  # на нормализованных = то же самое
        else:
            df["sbert_dot"] = (u_vecs * v_vecs).sum(axis=1)
            un = np.linalg.norm(u_vecs, axis=1)
            vn = np.linalg.norm(v_vecs, axis=1)
            df["sbert_cos"] = df["sbert_dot"] / (un * vn + 1e-9)
        df["sbert_l2"] = np.linalg.norm(u_vecs - v_vecs, axis=1)

        if self.include_vectors:
            # Одним concat: по одной колонке pandas строит 1536 копий таблицы.
            dim = u_vecs.shape[1]
            blocks = {"u": u_vecs, "v": v_vecs,
                      "diff": u_vecs - v_vecs, "hadamard": u_vecs * v_vecs}
            vec_df = pd.DataFrame(
                np.hstack(list(blocks.values())),
                columns=[f"sbert_{k}_{i:03d}" for k in blocks for i in range(dim)],
                index=df.index,
            )
            df = pd.concat([df, vec_df], axis=1)

        return df
