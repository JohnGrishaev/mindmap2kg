"""
Аналитический отчёт по таблице размеченных пар.

Считает то, что нужно для главы 2 ВКР и для принятия решений
о балансировке перед обучением:

  * распределение по relation (count, %)
  * уникальных seed-доноров на класс
  * вклад топ-10 seed-ов (выявить доминирующих доноров)
  * cross-class коллизии (одна пара — несколько меток)
  * самосвязи (u == v) — должны отсутствовать
  * длины меток узлов по классам

Использование:
    python scripts/analyze_annotations.py data/labeled/annotations.csv

Опционально:
    --out report.md     — записать отчёт в markdown-файл
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def analyze(df: pd.DataFrame) -> str:
    lines: list[str] = []
    P = lines.append

    P(f"# Аналитический отчёт по аннотациям\n")
    P(f"- Всего пар: **{len(df)}**")
    P(f"- Уникальных u-узлов: **{df['u_text'].nunique()}**")
    P(f"- Уникальных v-узлов: **{df['v_text'].nunique()}**")
    P(f"- Уникальных пар (u,v): **{df[['u_text','v_text']].drop_duplicates().shape[0]}**")
    if "seed" in df.columns:
        P(f"- Seed-ов в работе: **{df['seed'].nunique()}**")
    P("")

    # --- Распределение по классам --------------------------------------------
    P("## Распределение по relation\n")
    vc = df["relation"].value_counts()
    vc_pct = df["relation"].value_counts(normalize=True) * 100
    table = pd.concat([vc, vc_pct.round(2)], axis=1)
    table.columns = ["count", "pct"]
    P(table.to_markdown())
    P("")

    # --- Уникальных seed на класс --------------------------------------------
    if "seed" in df.columns:
        P("## Уникальных seed-доноров на класс\n")
        sp = df.groupby("relation")["seed"].nunique().sort_values(ascending=False)
        P(sp.to_frame("unique_seeds").to_markdown())
        P("")

        # --- Доминирующие доноры -------------------------------------------------
        P("## Топ-10 seed по вкладу пар\n")
        top = df.groupby("seed").size().sort_values(ascending=False).head(10)
        P(top.to_frame("pairs").to_markdown())
        P("")

        # Доминирование (доля топ-5 seed)
        top5_share = df.groupby("seed").size().sort_values(ascending=False).head(5).sum() / len(df)
        P(f"Топ-5 seed-ов суммарно дают **{top5_share*100:.1f}%** всех пар.")
        if top5_share > 0.6:
            P("⚠ Высокая концентрация: модель рискует выучить «словарь нескольких сидов».")
        P("")

    # --- Cross-class коллизии -----------------------------------------------
    P("## Cross-class коллизии (одна пара (u,v) → несколько relation)\n")
    pair_rel = df.groupby(["u_text", "v_text"])["relation"].nunique()
    collisions = pair_rel[pair_rel > 1]
    P(f"Коллизий: **{len(collisions)}**")
    if len(collisions) > 0:
        col_df = (df.merge(collisions.reset_index()[["u_text", "v_text"]],
                           on=["u_text", "v_text"])
                  .sort_values(["u_text", "v_text"]))
        P(col_df[["u_text", "v_text", "relation"]].to_markdown(index=False))
    P("")

    # --- Самосвязи -----------------------------------------------------------
    self_loops = df[df["u_text"] == df["v_text"]]
    P(f"## Самосвязи (u == v): **{len(self_loops)}**")
    if len(self_loops) > 0:
        P(self_loops[["u_text", "v_text", "relation"]].head(10).to_markdown(index=False))
    P("")

    # --- Длины меток ---------------------------------------------------------
    P("## Длины меток (число символов) по классам\n")
    df = df.copy()
    df["len_u"] = df["u_text"].str.len()
    df["len_v"] = df["v_text"].str.len()
    stats = df.groupby("relation")[["len_u", "len_v"]].agg(["mean", "median", "max"]).round(1)
    P(stats.to_markdown())
    P("")

    # --- Диагноз -------------------------------------------------------------
    P("## Диагноз\n")
    max_class = vc.idxmax()
    min_class = vc.idxmin()
    imbalance = vc.max() / max(vc.min(), 1)
    P(f"- Доминантный класс: **{max_class}** ({vc.max()} пар).")
    P(f"- Минимальный класс: **{min_class}** ({vc.min()} пар).")
    P(f"- Дисбаланс max/min: **{imbalance:.1f}×**.")
    if imbalance > 10:
        P("- ⚠ Требуется балансировка перед обучением "
          "(cap-per-class или class_weight='balanced').")
    classes_lt_50 = vc[vc < 50]
    if len(classes_lt_50):
        P(f"- ⚠ Классы с <50 примеров: **{list(classes_lt_50.index)}** — "
          f"расширь seed-список (BIOLOGY_SEEDS_TARGETED) или подключи LLM-разметку.")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Путь к annotations.csv")
    ap.add_argument("--out", help="Куда сохранить отчёт (markdown). "
                                  "Если не задан — печать в stdout.")
    args = ap.parse_args()

    df = pd.read_csv(args.path)
    report = analyze(df)

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Отчёт сохранён: {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
