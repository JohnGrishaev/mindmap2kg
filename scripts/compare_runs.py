"""
Сводная таблица по нескольким прогонам обучения.

Парсит markdown-отчёты из reports/*.md (формат, который пишет
scripts/train_classifier.py), собирает метрики в одну таблицу
и печатает её или сохраняет в CSV/MD.

Полезно для главы 2 ВКР: таблица «Сравнение конфигураций».

Использование:
    python scripts/compare_runs.py reports/exp_*.md \\
        --output reports/comparison.md
    python scripts/compare_runs.py reports/exp_*.md --csv reports/comparison.csv
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd


_F1_RE = re.compile(r"macro-F1:\s+\*\*([\d.]+)\*\*")
_WF1_RE = re.compile(r"weighted-F1:\s+\*\*([\d.]+)\*\*")
_TRAIN_RE = re.compile(r"train pairs:\s+\*\*(\d+)\*\*,\s+test pairs:\s+\*\*(\d+)\*\*")
_BACKEND_RE = re.compile(r"backend:\s+\*\*(\S+)\*\*")
_SBERT_RE = re.compile(r"use SBERT:\s+(True|False)")
_FEAT_RE = re.compile(r"признаков:\s+\*\*(\d+)\*\*")


def parse_report(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    def search(rx, group=1, default=None, cast=str):
        m = rx.search(text)
        if not m:
            return default
        try:
            return cast(m.group(group))
        except (ValueError, IndexError):
            return default

    train_m = _TRAIN_RE.search(text)
    return {
        "run_id":      path.stem,
        "backend":     search(_BACKEND_RE),
        "use_sbert":   search(_SBERT_RE),
        "n_features":  search(_FEAT_RE, cast=int),
        "n_train":     int(train_m.group(1)) if train_m else None,
        "n_test":      int(train_m.group(2)) if train_m else None,
        "macro_f1":    search(_F1_RE, cast=float),
        "weighted_f1": search(_WF1_RE, cast=float),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", nargs="+", help="Файлы reports/*.md")
    ap.add_argument("--output", default=None, help="Markdown-файл со сводкой")
    ap.add_argument("--csv", default=None, help="CSV-файл со сводкой")
    args = ap.parse_args()

    rows = []
    for p in args.reports:
        path = Path(p)
        if not path.exists():
            print(f"⚠ {p}: не найден", file=sys.stderr)
            continue
        row = parse_report(path)
        if row and row.get("macro_f1") is not None:
            rows.append(row)
        else:
            print(f"⚠ {p}: не удалось распарсить", file=sys.stderr)

    if not rows:
        print("Нет валидных отчётов", file=sys.stderr)
        return 1

    df = pd.DataFrame(rows).sort_values("macro_f1", ascending=False)
    md = "# Сравнение прогонов\n\n" + df.to_markdown(index=False)
    print(md)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(md + "\n", encoding="utf-8")
        print(f"\nMD: {args.output}", file=sys.stderr)
    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.csv, index=False)
        print(f"CSV: {args.csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
