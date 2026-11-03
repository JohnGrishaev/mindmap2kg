"""
Заглушка-классификатор: возвращает случайный класс из таксономии.

Нужна только для end-to-end проверки скелета пайплайна.
Заменяется на реальный классификатор (sklearn GBM, MLP, ...) на следующем шаге.
"""
from __future__ import annotations

import random
import pandas as pd

from ..core.base import BaseClassifier
from ..core.registry import register
from ..core.schemas import Prediction


@register("classifier", "dummy")
class DummyClassifier(BaseClassifier):
    def __init__(self, taxonomy: dict, seed: int = 42):
        self.classes = [r["id"] for r in taxonomy["relations"]]
        self.rng = random.Random(seed)

    def predict(self, df: pd.DataFrame) -> list[Prediction]:
        preds: list[Prediction] = []
        for _, row in df.iterrows():
            # случайные баллы, потом softmax-нормализация
            raw_scores = {c: self.rng.random() for c in self.classes}
            total = sum(raw_scores.values())
            scores = {c: v / total for c, v in raw_scores.items()}
            winner = max(scores, key=scores.get)
            preds.append(Prediction(
                pair_id=row["pair_id"],
                relation=winner,
                confidence=scores[winner],
                all_scores=scores,
            ))
        return preds
