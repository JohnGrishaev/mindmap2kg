"""
Генератор синтетических ментальных карт из небольшой биологической онтологии.
Используется для тестирования пайплайна, пока нет реальных карт от студентов.

На выходе — файлы FreeMind (.mm) в data/raw/.

Поскольку структура онтологии задана вручную с известными типами связей,
эти карты также служат seed-данными для будущей обучающей выборки
(см. data/labeled/annotations.parquet, source='synthetic_seed').
"""
from __future__ import annotations

import argparse
import re
import uuid
from pathlib import Path
from lxml import etree


# Микро-онтология биологии. Структура: parent -> [(child, relation_type), ...]
# Типы связей соответствуют configs/taxonomy.yaml.
ONTOLOGY: dict[str, list[tuple[str, str]]] = {
    "Биология": [
        ("Клетка", "has_example"),
        ("Растение", "has_example"),
        ("Млекопитающее", "has_example"),
        ("Эволюция", "associated_with"),
    ],
    "Клетка": [
        ("Митохондрия",        "has_part"),
        ("Рибосома",           "has_part"),
        ("Ядро",               "has_part"),
        ("Клеточная мембрана", "has_part"),
        ("Полупроницаемость",  "has_property"),
    ],
    "Митохондрия": [
        ("Кристы",                 "has_part"),
        ("Митохондриальная ДНК",   "has_part"),
        ("Матрикс",                "has_part"),
        ("Синтез АТФ",             "has_function"),
    ],
    "Растение": [
        ("Корень",     "has_part"),
        ("Стебель",    "has_part"),
        ("Лист",       "has_part"),
        ("Цветок",     "has_part"),
        ("Фотосинтез", "has_function"),
    ],
    "Лист": [
        ("Хлоропласт", "has_part"),
        ("Устьица",    "has_part"),
        ("Зелёный",    "has_property"),
    ],
    "Хлоропласт": [
        ("Хлорофилл", "has_part"),
        ("Тилакоид",  "has_part"),
        ("Фотосинтез","has_function"),
    ],
    "Млекопитающее": [
        ("Кошка",         "has_example"),
        ("Собака",        "has_example"),
        ("Кит",           "has_example"),
        ("Теплокровность","has_property"),
    ],
    "Эволюция": [
        ("Мутация",         "causes"),
        ("Естественный отбор", "associated_with"),
        ("Изменение вида",  "causes"),
    ],
    "Митоз": [
        ("Профаза",   "has_part"),
        ("Метафаза",  "has_part"),
        ("Анафаза",   "has_part"),
        ("Телофаза",  "has_part"),
    ],
    "Профаза":  [("Метафаза", "precedes")],
    "Метафаза": [("Анафаза",  "precedes")],
    "Анафаза":  [("Телофаза", "precedes")],
}


def slugify(text: str) -> str:
    """Безопасное имя для ID/файла."""
    s = re.sub(r"\s+", "_", text.strip())
    s = re.sub(r"[^\w]", "", s, flags=re.UNICODE)
    return s


def build_subtree(root_label: str, max_depth: int = 4) -> etree._Element:
    """Построить FreeMind-дерево, начиная с указанного корня."""
    visited: set[str] = set()

    def make_node(label: str, depth: int) -> etree._Element:
        nid = f"ID_{slugify(label)}_{uuid.uuid4().hex[:6]}"
        node = etree.Element("node", TEXT=label, ID=nid)
        if depth >= max_depth or label in visited:
            return node
        visited.add(label)
        for child_label, rel_type in ONTOLOGY.get(label, []):
            child_node = make_node(child_label, depth + 1)
            # Сохраняем "истинную" разметку как атрибут — её можно потом
            # использовать как gold label для обучения.
            child_node.set("GOLD_RELATION", rel_type)
            node.append(child_node)
        return node

    return make_node(root_label, 0)


def save_freemind(root_label: str, out_path: Path) -> None:
    map_elem = etree.Element("map", version="1.0.1")
    map_elem.append(build_subtree(root_label))
    tree = etree.ElementTree(map_elem)
    tree.write(str(out_path), pretty_print=True, xml_declaration=True, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/raw", help="Куда складывать .mm")
    ap.add_argument("--roots", nargs="*",
                    default=["Биология", "Клетка", "Растение", "Митоз"],
                    help="С каких корней генерировать карты")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for root_label in args.roots:
        fname = f"synthetic_{slugify(root_label).lower()}.mm"
        out_path = out_dir / fname
        save_freemind(root_label, out_path)
        print(f"  ✓ {out_path}")

    print(f"\nГотово. Сгенерировано: {len(args.roots)} карт в {out_dir}/")


if __name__ == "__main__":
    main()
