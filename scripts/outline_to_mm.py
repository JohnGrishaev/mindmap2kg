"""
Текстовые схемы ментальных карт → файлы FreeMind (.mm) с эталонной разметкой.

Формат схемы (.txt, UTF-8). Карты разделяются строкой "# <имя карты>";
вложенность — отступ в 2 пробела; тип связи с родителем — код после " :".

    # Клетка
    Клетка
      Ядро :p
        Ядрышко :p
      Функции :a
        Хранение наследственной информации :f

Коды типов связей:
    p — has_part        e — has_example     r — has_property
    f — has_function    c — causes          s — precedes
    a — associated_with (в т. ч. связь с группирующим узлом «Строение», «Виды» …)

Тип пишется в атрибут GOLD_RELATION узла-потомка — так же, как в
scripts/generate_synthetic_maps.py. Парсер freemind его просто сохраняет в
metadata, на работу пайплайна атрибут не влияет.

Пример:
    python scripts/outline_to_mm.py data/generated/outlines/*.txt \\
        --out-dir data/generated/maps
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lxml import etree

CODES = {"p": "has_part", "e": "has_example", "r": "has_property",
         "f": "has_function", "c": "causes", "s": "precedes",
         "a": "associated_with"}
LINE_RE = re.compile(r"^(?P<indent> *)(?P<text>.+?)(?: :(?P<code>[a-z]))?\s*$")


def slug(text: str) -> str:
    return re.sub(r"[^\w\-]+", "_", text.strip().lower()).strip("_")[:60]


def parse_outlines(path: Path) -> list[tuple[str, etree._Element]]:
    """Возвращает [(имя карты, корневой <node>)]."""
    maps: list[tuple[str, etree._Element]] = []
    name, stack, counter = None, [], 0
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        if raw.startswith("# "):
            name, stack = raw[2:].strip(), []
            continue
        m = LINE_RE.match(raw)
        level, text, code = len(m["indent"]) // 2, m["text"].strip(), m["code"]
        if len(m["indent"]) % 2:
            raise ValueError(f"{path}:{lineno}: отступ должен быть кратен 2")
        node = etree.Element("node", TEXT=text, ID=f"ID_{counter}")
        counter += 1
        if level == 0:
            if code:
                raise ValueError(f"{path}:{lineno}: у корня не должно быть типа связи")
            if name is None:
                raise ValueError(f"{path}:{lineno}: нет заголовка '# имя карты'")
            maps.append((name, node))
            stack = [node]
            continue
        if code not in CODES:
            raise ValueError(f"{path}:{lineno}: неизвестный или пропущенный код '{code}'")
        if level > len(stack):
            raise ValueError(f"{path}:{lineno}: отступ больше, чем на один уровень")
        stack = stack[:level]
        stack[-1].append(node)
        node.set("GOLD_RELATION", CODES[code])
        stack.append(node)
    return maps


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("outlines", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("data/generated/maps"))
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    n_maps = n_edges = 0
    seen: set[str] = set()
    for path in args.outlines:
        for name, root in parse_outlines(path):
            fname = slug(name)
            if fname in seen:
                raise ValueError(f"Повтор имени карты: {name}")
            seen.add(fname)
            mm = etree.Element("map", version="1.0.1")
            mm.append(root)
            etree.ElementTree(mm).write(str(args.out_dir / f"{fname}.mm"),
                                        encoding="utf-8", xml_declaration=True,
                                        pretty_print=True)
            n_maps += 1
            n_edges += len(root.xpath(".//node"))
    print(f"Карт: {n_maps}, связей: {n_edges} → {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
