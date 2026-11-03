"""Тесты модуля балансировки."""
import pandas as pd
import pytest

from mindmap2kg.annotation.balance import (
    balance, cap_per_class, cap_per_seed, drop_collisions,
)


@pytest.fixture
def df():
    return pd.DataFrame([
        # seed=A, has_example x5
        {"u_text": "A", "v_text": f"a{i}", "relation": "has_example", "seed": "A"}
        for i in range(5)
    ] + [
        # seed=B, has_part x3
        {"u_text": "B", "v_text": f"b{i}", "relation": "has_part", "seed": "B"}
        for i in range(3)
    ] + [
        # коллизия: (X,Y) встречается с двумя relation
        {"u_text": "X", "v_text": "Y", "relation": "has_example", "seed": "A"},
        {"u_text": "X", "v_text": "Y", "relation": "has_part",    "seed": "B"},
    ])


def test_cap_per_seed_caps(df):
    out = cap_per_seed(df, cap=2)
    counts = out.groupby("seed").size()
    assert all(counts <= 2)


def test_cap_per_class_caps(df):
    out = cap_per_class(df, cap=2)
    counts = out["relation"].value_counts()
    assert all(counts <= 2)


def test_drop_collisions_removes_pair(df):
    out = drop_collisions(df)
    pair_count = out[(out["u_text"] == "X") & (out["v_text"] == "Y")].shape[0]
    assert pair_count == 0


def test_balance_full(df):
    out = balance(df, per_seed=2, per_class=10, drop_collisions_flag=True)
    # коллизий нет
    pair_rel = out.groupby(["u_text", "v_text"])["relation"].nunique()
    assert (pair_rel > 1).sum() == 0
    # cap-per-seed работает
    assert all(out.groupby("seed").size() <= 2)
