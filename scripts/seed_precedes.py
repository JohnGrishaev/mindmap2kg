"""
Генератор пар класса `precedes` из курируемого YAML-файла.

Без LLM, без сети. Подходит, когда:
  * у автора нет доступа к LLM API,
  * нужна полная воспроизводимость (для ВКР это плюс),
  * Wikidata не покрывает класс precedes (см. probe v2).

Источник: configs/biology_sequences.yaml — для каждого процесса задана
упорядоченная цепочка этапов. Соседние пары становятся precedes-парами.

Опциональный режим --with-has-part добавляет также пары
"<процесс> has_part <этап>" для каждого этапа. Это семантически верно
(процесс состоит из этапов) и сразу даёт +N has_part пар. Включать
осторожно — может смешать сигнал с настоящими has_part из Wikidata.

Использование:
    python scripts/seed_precedes.py \\
        --sequences configs/biology_sequences.yaml \\
        --output data/labeled/precedes_pairs.csv

    # с has_part-парами:
    python scripts/seed_precedes.py --with-has-part

Затем склеить с основной таблицей через scripts/merge_annotations.py.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml


def build_pairs(spec: dict, with_has_part: bool = False) -> pd.DataFrame:
    source = spec.get("source", "curated")
    version = spec.get("version", "unknown")
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    rows: list[dict] = []
    for proc in spec.get("processes", []):
        topic = proc["topic"]
        stages = [str(s).strip() for s in proc.get("stages", []) if str(s).strip()]
        if len(stages) < 2:
            continue

        # precedes-пары: соседние этапы
        for a, b in zip(stages[:-1], stages[1:]):
            if a == b:
                continue
            rows.append({
                "u_text":  a,
                "v_text":  b,
                "relation": "precedes",
                "source":   source,
                "seed":     topic,
                "curated_version": version,
                "extracted_ts": ts,
            })

        # опционально has_part: процесс → каждый этап
        if with_has_part:
            for stage in stages:
                if stage == topic:
                    continue
                rows.append({
                    "u_text":  topic,
                    "v_text":  stage,
                    "relation": "has_part",
                    "source":   source,
                    "seed":     topic,
                    "curated_version": version,
                    "extracted_ts": ts,
                })

    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sequences", default="configs/biology_sequences.yaml")
    ap.add_argument("--output", default="data/labeled/precedes_pairs.csv")
    ap.add_argument("--with-has-part", action="store_true",
                    help="Дополнительно сгенерировать has_part-пары "
                         "(процесс → этап)")
    args = ap.parse_args()

    spec_path = Path(args.sequences)
    if not spec_path.exists():
        print(f"Файл не найден: {spec_path}", file=sys.stderr)
        return 1
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))

    df = build_pairs(spec, with_has_part=args.with_has_part)
    if df.empty:
        print("Не сгенерировано ни одной пары", file=sys.stderr)
        return 1

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")

    print(f"=== Курируемая разметка ===")
    print(f"  Источник: {args.sequences}")
    print(f"  Процессов: {len(spec.get('processes', []))}")
    print(f"  Всего пар: {len(df)}")
    print(f"  По классам:")
    for rel, n in df["relation"].value_counts().items():
        print(f"    {rel:<14} {n:>5}")
    print(f"\n  Сохранено в: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
