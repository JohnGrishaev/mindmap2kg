"""
Склейка нескольких таблиц аннотаций в одну.

Полезно для объединения:
  * data/labeled/annotations.csv  (из Wikidata)
  * data/labeled/precedes_pairs.csv (из curated YAML или LLM)
  * data/labeled/annotations_validated.csv (после LLM-валидации)
  → data/labeled/annotations_merged.csv

Правила склейки:
  * берётся объединение всех колонок (отсутствующие — пустые);
  * после конкатенации удаляются дубликаты по (u_text, v_text, relation);
  * приоритет источника при коллизиях (одна и та же пара u→v разных
    relation) — по порядку файлов в командной строке: первая входная
    таблица побеждает. Конкурирующие записи логируются.

Использование:
    python scripts/merge_annotations.py \\
        data/labeled/annotations.csv \\
        data/labeled/precedes_pairs.csv \\
        --output data/labeled/annotations_merged.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="CSV-файлы для склейки")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    frames = []
    for p in args.inputs:
        path = Path(p)
        if not path.exists():
            print(f"⚠ пропуск: {p} не найден", file=sys.stderr)
            continue
        df = pd.read_csv(path)
        df["_origin"] = path.name
        frames.append(df)
        print(f"  {path}: {len(df)} строк")

    if not frames:
        print("Нет входных файлов", file=sys.stderr)
        return 1

    merged = pd.concat(frames, ignore_index=True, sort=False)
    print(f"\nИтого до дедупликации: {len(merged)}")

    # Полные дубликаты (u,v,relation) — оставляем первое вхождение
    before = len(merged)
    merged = merged.drop_duplicates(subset=["u_text", "v_text", "relation"],
                                     keep="first")
    print(f"После удаления точных дублей: {len(merged)} (-{before - len(merged)})")

    # Коллизии: один (u,v) с разным relation
    pair_rel = merged.groupby(["u_text", "v_text"])["relation"].nunique()
    collisions = pair_rel[pair_rel > 1]
    if len(collisions) > 0:
        print(f"\n⚠ Коллизий (одна пара — разный relation): {len(collisions)}")
        # Берём первый по порядку входных файлов
        first_only = merged.drop_duplicates(subset=["u_text", "v_text"],
                                             keep="first")
        dropped = len(merged) - len(first_only)
        print(f"  Удалено младших записей: {dropped}")
        merged = first_only

    merged = merged.drop(columns=["_origin"], errors="ignore")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out, index=False, encoding="utf-8")

    print(f"\n=== Готово ===")
    print(f"  Итог: {len(merged)} пар")
    print(f"  По классам:")
    for rel, n in merged["relation"].value_counts().items():
        print(f"    {rel:<18} {n:>5}")
    print(f"\n  Сохранено в: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
