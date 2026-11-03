"""Тесты LLM-аннотатора с MockProvider — без сети, детерминированно."""
from __future__ import annotations

import json

import pandas as pd

from mindmap2kg.annotation.llm_annotator import (
    LLMAnnotator,
    MockProvider,
    _extract_json,
)


def test_extract_json_plain():
    assert _extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_with_fences():
    txt = "```json\n{\"a\": 2}\n```"
    assert _extract_json(txt) == {"a": 2}


def test_extract_json_with_preamble():
    txt = "Вот ответ: {\"a\": 3, \"b\": [1,2]}"
    assert _extract_json(txt) == {"a": 3, "b": [1, 2]}


def test_extract_json_invalid():
    assert _extract_json("полный мусор без json") is None


def test_validate_pair_correct():
    annot = LLMAnnotator(MockProvider(validate_verdict="correct"))
    res = annot.validate_pair("клетка", "митохондрия", "has_part")
    assert res.verdict == "correct"
    assert res.suggested_relation == ""


def test_validate_pair_wrong_suggests():
    annot = LLMAnnotator(MockProvider(validate_verdict="wrong",
                                      suggested="has_function"))
    res = annot.validate_pair("митохондрия", "синтез АТФ", "has_part")
    assert res.verdict == "wrong"
    assert res.suggested_relation == "has_function"


def test_validate_pair_unknown_suggestion_dropped():
    annot = LLMAnnotator(MockProvider(validate_verdict="wrong",
                                      suggested="бессмысленный_класс"))
    res = annot.validate_pair("a", "b", "has_part")
    # неизвестный класс должен быть выкинут
    assert res.suggested_relation == ""


def test_validate_pairs_only_relations():
    df = pd.DataFrame([
        {"u_text": "клетка",     "v_text": "митохондрия", "relation": "has_part"},
        {"u_text": "митохондрия","v_text": "АТФ",         "relation": "has_function"},
        {"u_text": "вода",       "v_text": "прозрачность","relation": "has_property"},
    ])
    annot = LLMAnnotator(MockProvider(validate_verdict="correct"))
    out = annot.validate_pairs(df, only_relations=["has_function", "has_property"],
                                verbose=False)
    # первая строка не валидировалась
    assert out.loc[0, "llm_verdict"] == ""
    assert out.loc[1, "llm_verdict"] == "correct"
    assert out.loc[2, "llm_verdict"] == "correct"


def test_generate_precedes_pairs():
    stages = ["профаза", "метафаза", "анафаза", "телофаза"]
    annot = LLMAnnotator(MockProvider(precedes_stages=stages))
    df = annot.generate_precedes(topics=["митоз"], verbose=False)
    # 4 этапа → 3 пары precedes
    assert len(df) == 3
    assert all(df["relation"] == "precedes")
    assert df.iloc[0]["u_text"] == "профаза"
    assert df.iloc[0]["v_text"] == "метафаза"
    assert df.iloc[-1]["v_text"] == "телофаза"
    assert all(df["source"] == "llm")
    assert all(df["seed"] == "митоз")
