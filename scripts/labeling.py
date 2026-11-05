"""
Разметка типов связей в настоящих ментальных картах.

Два шага:

1. export — все .mm-карты папки → одна таблица Excel (.xlsx): по строке на
   связь «родитель → потомок», с предсказанием модели и пустой колонкой
   gold, куда вписывается правильный тип связи.

       python scripts/labeling.py export data/real/maps \\
           --config configs/experiments/exp_maps.yaml \\
           --output data/real/to_label.xlsx

2. apply — проверенная таблица → копии карт с атрибутом GOLD_RELATION
   (тот же формат, что у сгенерированных карт). Дальше их можно прогнать
   через scripts/extract_labeled_pairs.py и использовать как тестовый набор.

       python scripts/labeling.py apply data/real/to_label.xlsx \\
           --maps-dir data/real/maps --out-dir data/real/labeled_maps

Допустимые значения gold: has_part, has_example, has_property, has_function,
causes, precedes, associated_with. Пустая клетка gold — связь пропускается.
Открывать и сохранять таблицу можно в Excel: формат .xlsx не ломает
кириллицу (в отличие от CSV).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from lxml import etree

import mindmap2kg  # noqa: F401  — регистрирует плагины
from mindmap2kg.core.config import load_config, load_taxonomy
from mindmap2kg.core.registry import get

RELATIONS = ["has_part", "has_example", "has_property", "has_function",
             "causes", "precedes", "associated_with"]
COLUMNS = ["map", "u_id", "v_id", "parent", "child", "predicted", "confidence", "gold", "comment"]


def predict_map(path: Path, cfg, taxonomy) -> pd.DataFrame:
    mm = get("parser", cfg.parser.name)(**cfg.parser.options).parse(path)
    pairs = get("pairing", cfg.pairing.name)(**cfg.pairing.options).extract(mm)
    df = pd.DataFrame([p.__dict__ for p in pairs])
    if df.empty:
        return df
    for f in cfg.features:
        df = get("feature", f.name)(**f.options).transform(df, mm)
    clf = get("classifier", cfg.classifier.name)(taxonomy=taxonomy, **cfg.classifier.options)
    preds = {p.pair_id: p for p in clf.predict(df)}
    gold = {n.id: n.metadata.get("GOLD_RELATION", "") for n in mm.nodes}
    return pd.DataFrame({
        "map": path.name,
        "u_id": df["u_id"], "v_id": df["v_id"],
        "parent": df["u_text"], "child": df["v_text"],
        "predicted": [preds[i].relation for i in df["pair_id"]],
        "confidence": [round(preds[i].confidence, 2) for i in df["pair_id"]],
        "gold": df["v_id"].map(gold).fillna(""),
        "comment": "",
    })


def cmd_export(args) -> int:
    cfg = load_config(args.config)
    taxonomy = load_taxonomy(cfg.taxonomy)
    files = sorted(Path(args.maps_dir).glob("*.mm"))
    if not files:
        print(f"Нет .mm-файлов в {args.maps_dir}", file=sys.stderr)
        return 1
    df = pd.concat([predict_map(f, cfg, taxonomy) for f in files], ignore_index=True)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as xw:
        df[COLUMNS].to_excel(xw, sheet_name="pairs", index=False)
        pd.DataFrame({"gold": RELATIONS, "значение": [
            "часть – целое (Клетка → Ядро)",
            "род – вид, пример (Органоиды → Митохондрия)",
            "свойство (Роговица → Прозрачность)",
            "функция (Митохондрия → Синтез АТФ)",
            "причина – следствие (Курение → Рак легких)",
            "следующий этап (Профаза → Метафаза)",
            "прочее, в т. ч. связь с узлом-заголовком (Клетка → Строение)",
        ]}).to_excel(xw, sheet_name="типы связей", index=False)
        ws = xw.sheets["pairs"]
        for col, width in zip("ABCDEFGHI", [22, 8, 8, 32, 32, 14, 11, 16, 30]):
            ws.column_dimensions[col].width = width
        ws.freeze_panes = "A2"
    print(f"Карт: {len(files)}, связей: {len(df)} → {out}")
    return 0


def cmd_apply(args) -> int:
    df = pd.read_excel(args.table, sheet_name="pairs", dtype=str).fillna("")
    bad = df[(df["gold"] != "") & ~df["gold"].isin(RELATIONS)]
    if len(bad):
        print("Недопустимые значения gold:\n" + bad[["map", "parent", "child", "gold"]].to_string(),
              file=sys.stderr)
        return 1
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n_set = 0
    for name, g in df.groupby("map"):
        src = Path(args.maps_dir) / name
        tree = etree.parse(str(src))
        labels = dict(zip(g["v_id"], g["gold"]))
        # ID узлов назначает парсер: из атрибута ID, иначе n<порядковый номер>
        for i, node in enumerate(tree.getroot().iter("node")):
            nid = node.get("ID") or f"n{i}"
            if labels.get(nid):
                node.set("GOLD_RELATION", labels[nid])
                n_set += 1
        tree.write(str(out_dir / name), encoding="utf-8", xml_declaration=True)
    print(f"Размечено связей: {n_set} из {len(df)} → {out_dir}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export", help="карты → таблица для разметки")
    e.add_argument("maps_dir")
    e.add_argument("--config", default="configs/experiments/exp_maps.yaml")
    e.add_argument("--output", default="data/real/to_label.xlsx")
    a = sub.add_parser("apply", help="размеченная таблица → карты с GOLD_RELATION")
    a.add_argument("table")
    a.add_argument("--maps-dir", required=True)
    a.add_argument("--out-dir", default="data/real/labeled_maps")
    args = ap.parse_args()
    return cmd_export(args) if args.cmd == "export" else cmd_apply(args)


if __name__ == "__main__":
    sys.exit(main())
