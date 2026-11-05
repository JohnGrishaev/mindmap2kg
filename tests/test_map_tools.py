"""Тесты конвертера схем и выгрузки размеченных пар."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from extract_labeled_pairs import map_to_pairs  # noqa: E402
from outline_to_mm import parse_outlines  # noqa: E402
from lxml import etree  # noqa: E402

OUTLINE = """# Клетка
Клетка
  Строение :a
    Ядро :p
    Митохондрия :p
      Синтез АТФ :f
  Профаза :p
    Метафаза :s
"""


def _write_map(tmp_path, text=OUTLINE):
    src = tmp_path / "o.txt"
    src.write_text(text, encoding="utf-8")
    (name, root), = parse_outlines(src)
    mm = etree.Element("map"); mm.append(root)
    out = tmp_path / "kletka.mm"
    etree.ElementTree(mm).write(str(out), encoding="utf-8", xml_declaration=True)
    return out


def test_outline_roundtrip_to_pairs(tmp_path):
    df = map_to_pairs(_write_map(tmp_path), "test")
    got = set(zip(df.u_text, df.v_text, df.relation))
    assert ("Строение", "Ядро", "has_part") in got
    assert ("Митохондрия", "Синтез АТФ", "has_function") in got
    assert ("Профаза", "Метафаза", "precedes") in got
    assert set(df.seed) == {"kletka"}
    row = df[df.v_text == "Синтез АТФ"].iloc[0]
    assert row.topo_depth_v == 3 and bool(row.topo_v_is_leaf)


def test_outline_rejects_unknown_code(tmp_path):
    with pytest.raises(ValueError, match="код"):
        _write_map(tmp_path, "# X\nКорень\n  Лист :z\n")
