"""
CLI для сбора размеченных пар из Wikidata.

Использование:
    # Дефолтный список из 30 биологических терминов
    python scripts/extract_wikidata.py

    # Свой список через файл (одно слово на строку)
    python scripts/extract_wikidata.py --seeds-file my_seeds.txt

    # Свой output-путь
    python scripts/extract_wikidata.py --output data/labeled/wikidata_v1.csv

    # Тихий режим
    python scripts/extract_wikidata.py --quiet

Прогон по дефолтному списку (30 терминов × 8 запросов на термин)
занимает ~5-7 минут.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import mindmap2kg  # noqa: F401
from mindmap2kg.annotation.wikidata_extractor import (
    BIOLOGY_SEEDS_DEFAULT,
    BIOLOGY_SEEDS_TARGETED,
    BIOLOGY_SEEDS_FULL,
    WikidataExtractor,
)

SEED_SETS = {
    "default":  BIOLOGY_SEEDS_DEFAULT,   # 31 базовый seed
    "targeted": BIOLOGY_SEEDS_TARGETED,  # ~40 seed под минорные классы
    "full":     BIOLOGY_SEEDS_FULL,      # default + targeted
}


def main():
    ap = argparse.ArgumentParser(description="Сбор пар из Wikidata по биологии")
    ap.add_argument("--taxonomy", default="configs/taxonomy.yaml")
    ap.add_argument("--output",   default="data/labeled/annotations.csv")
    ap.add_argument("--seeds-file", default=None,
                    help="Файл со списком seed-терминов (по одному на строку). "
                         "Если задан — приоритет над --seeds-set.")
    ap.add_argument("--seeds-set", default="full",
                    choices=list(SEED_SETS.keys()),
                    help="Какой встроенный список использовать (default: full).")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if args.seeds_file:
        seeds = [s.strip() for s in Path(args.seeds_file).read_text(encoding="utf-8").splitlines()
                 if s.strip() and not s.startswith("#")]
    else:
        seeds = SEED_SETS[args.seeds_set]

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"=== Wikidata extraction ===")
    print(f"  Таксономия:  {args.taxonomy}")
    print(f"  Seed-терминов: {len(seeds)}")
    print(f"  Выход:       {out_path}")
    print()

    extractor = WikidataExtractor(taxonomy_path=args.taxonomy)
    df = extractor.extract(seeds, verbose=not args.quiet)

    if df.empty:
        print("\nОШИБКА: не удалось извлечь ни одной пары")
        sys.exit(1)

    df.to_csv(out_path, index=False, encoding='utf-8')

    print(f"\n=== Готово ===")
    print(f"  Всего пар: {len(df)}")
    print(f"  По классам:")
    for rel, n in df["relation"].value_counts().items():
        print(f"    {rel:<18} {n:>5}")
    print(f"\n  Сохранено в: {out_path}")


if __name__ == "__main__":
    main()
