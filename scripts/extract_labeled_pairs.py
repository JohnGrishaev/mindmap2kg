"""
Размеченные ментальные карты (.mm с атрибутом GOLD_RELATION) → таблица пар.

Каждое ребро карты становится строкой с колонками u_text, v_text, relation,
seed (имя карты — по нему идёт групповое разбиение), source и признаками
топологии topo_*, вычисленными по настоящему дереву карты тем же
экстрактором, что и в пайплайне. Ребра без GOLD_RELATION пропускаются.

Пример:
    python scripts/extract_labeled_pairs.py data/generated/maps \\
        --source llm_generated --output data/labeled/maps_llm.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

import mindmap2kg  # noqa: F401  — регистрирует плагины
from mindmap2kg.core.registry import get


def map_to_pairs(path: Path, source: str) -> pd.DataFrame:
    mm = get("parser", "freemind")().parse(path)
    pairs = get("pairing", "parent_child")().extract(mm)
    df = pd.DataFrame([p.__dict__ for p in pairs])
    if df.empty:
        return df
    df = get("feature", "topology")().transform(df, mm)
    gold = {n.id: n.metadata.get("GOLD_RELATION") for n in mm.nodes}
    df["relation"] = df["v_id"].map(gold)
    df["seed"] = path.stem
    df["source"] = source
    return df.dropna(subset=["relation"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("maps_dir", type=Path)
    ap.add_argument("--source", default="llm_generated")
    ap.add_argument("--output", type=Path, default=Path("data/labeled/maps_llm.csv"))
    args = ap.parse_args()
    files = sorted(args.maps_dir.glob("*.mm"))
    if not files:
        print(f"Нет .mm-файлов в {args.maps_dir}", file=sys.stderr)
        return 1
    df = pd.concat([map_to_pairs(f, args.source) for f in files], ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8")
    print(f"Карт: {len(files)}, пар: {len(df)} → {args.output}")
    print(df["relation"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
