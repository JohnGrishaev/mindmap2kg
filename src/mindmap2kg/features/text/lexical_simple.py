"""
Простые лексические признаки на основе сырого текста меток узлов.

Не требуют обучения и моделей. Это baseline-фичи: длина текста,
количество слов, Жаккар по словам (доля общих слов в паре).

Когда добавим SBERT/RuBERT — те будут отдельным фичером 'sbert',
а эти останутся полезной "дешёвой" опцией для быстрых экспериментов.
"""
from __future__ import annotations

import pandas as pd

from ...core.base import BaseFeature
from ...core.registry import register
from ...core.schemas import MindMap


@register("feature", "lexical_simple")
class LexicalSimpleFeatures(BaseFeature):
    def transform(self, df: pd.DataFrame, mm: MindMap) -> pd.DataFrame:
        df = df.copy()
        df["lex_len_u"]   = df["u_text"].str.len()
        df["lex_len_v"]   = df["v_text"].str.len()
        df["lex_words_u"] = df["u_text"].str.split().str.len()
        df["lex_words_v"] = df["v_text"].str.split().str.len()
        df["lex_jaccard_words"] = df.apply(
            lambda r: self._jaccard(r["u_text"], r["v_text"]), axis=1)
        df["lex_jaccard_chars"] = df.apply(
            lambda r: self._jaccard_chars(r["u_text"], r["v_text"]), axis=1)
        return df

    @staticmethod
    def _jaccard(a: str, b: str) -> float:
        s1 = set(a.lower().split())
        s2 = set(b.lower().split())
        if not s1 or not s2:
            return 0.0
        return len(s1 & s2) / len(s1 | s2)

    @staticmethod
    def _jaccard_chars(a: str, b: str) -> float:
        s1 = set(a.lower())
        s2 = set(b.lower())
        if not s1 or not s2:
            return 0.0
        return len(s1 & s2) / len(s1 | s2)
