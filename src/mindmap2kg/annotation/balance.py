"""
Балансировка размеченной таблицы перед обучением.

Делает две независимые операции:
  1. cap_per_seed: на одного seed-донора оставляем не более N пар (рандомно).
     Лечит ситуацию, когда один seed (например, "белок" → 707 пар) забивает
     модель словарём своей подобласти.
  2. cap_per_class: на один класс оставляем не более M пар.
     Лечит мажорный дисбаланс has_example vs остальные.

Обе операции стабильны: используют seed для воспроизводимости.
Возвращают новый DataFrame, исходный не меняют.
"""
from __future__ import annotations

import pandas as pd


def cap_per_seed(df: pd.DataFrame, cap: int, random_state: int = 42) -> pd.DataFrame:
    """Ограничить число пар на seed-донора."""
    if "seed" not in df.columns:
        return df
    parts = []
    for _, g in df.groupby("seed", sort=False):
        if len(g) > cap:
            g = g.sample(n=cap, random_state=random_state)
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def cap_per_class(df: pd.DataFrame, cap: int, random_state: int = 42) -> pd.DataFrame:
    """Ограничить число пар на класс."""
    parts = []
    for _, g in df.groupby("relation", sort=False):
        if len(g) > cap:
            g = g.sample(n=cap, random_state=random_state)
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def drop_collisions(df: pd.DataFrame) -> pd.DataFrame:
    """Удалить пары (u,v), которым приписано >1 разных relation."""
    pair_rel = df.groupby(["u_text", "v_text"])["relation"].nunique()
    bad = pair_rel[pair_rel > 1].index
    if len(bad) == 0:
        return df
    mask = df.set_index(["u_text", "v_text"]).index.isin(bad)
    return df.loc[~mask].reset_index(drop=True)


def balance(df: pd.DataFrame,
            per_seed: int | None = 100,
            per_class: int | None = 300,
            drop_collisions_flag: bool = True,
            random_state: int = 42) -> pd.DataFrame:
    """
    Полный пайплайн балансировки.

    Порядок: drop_collisions → cap_per_seed → cap_per_class.
    Аргументы со значением None отключают соответствующий шаг.
    """
    out = df.copy()
    if drop_collisions_flag:
        out = drop_collisions(out)
    if per_seed is not None:
        out = cap_per_seed(out, per_seed, random_state)
    if per_class is not None:
        out = cap_per_class(out, per_class, random_state)
    return out.reset_index(drop=True)
