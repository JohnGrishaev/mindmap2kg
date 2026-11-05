"""
Оценка классификатора на повторных групповых разбиениях.

Один прогон train_classifier.py даёт одно разбиение, и при ~100 группах
(seed-терминах) метрики сильно зависят от того, какие группы попали в тест.
Этот скрипт повторяет GroupShuffleSplit N раз (random_state = 0..N-1) и
печатает среднее и стандартное отклонение macro-F1 / weighted-F1 и F1 по
классам, а также суммарную матрицу ошибок по всем повторам.

Наборы признаков (--features, можно несколько):
  lex        — lexical_simple (6 признаков)
  lex_sbert  — lex + sbert_cos, sbert_dot, sbert_l2
  lex_svec   — lex + скаляры SBERT + полные векторы u, v, u−v, u⊙v (1536)

Пример (полная таблица для ВКР):
    python scripts/evaluate_repeated.py \\
        --annotations data/labeled/annotations_v1.csv \\
        --features lex lex_sbert lex_svec \\
        --backends tfidf_logreg rf logreg --n-repeats 20 \\
        --out reports/repeated_eval.md
"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mindmap2kg  # noqa: F401  — регистрирует плагины
from mindmap2kg.annotation.balance import balance
from mindmap2kg.classifiers.sklearn_wrapper import (
    BACKENDS, _make_estimator, fit_estimator, make_input, select_feature_columns,
)
from mindmap2kg.core.registry import get
from train_classifier import make_stub_mindmap

warnings.filterwarnings("ignore", category=UserWarning)


def build(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    work = df.copy()
    work["pair_id"] = [f"p_{i}" for i in range(len(work))]
    work["u_id"] = work["pair_id"] + "_u"
    work["v_id"] = work["pair_id"] + "_v"
    mm = make_stub_mindmap(work)
    work = get("feature", "lexical_simple")().transform(work, mm)
    if mode in {"lex_sbert", "lex_svec"}:
        work = get("feature", "sbert")(include_vectors=(mode == "lex_svec")).transform(work, mm)
    return work


def evaluate(feats: pd.DataFrame, backend: str, n_rep: int, test_size: float):
    from sklearn.metrics import (confusion_matrix, f1_score,
                                 precision_recall_fscore_support)
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.utils.class_weight import compute_sample_weight

    cols = select_feature_columns(feats)
    labels = sorted(feats["relation"].unique())
    X = make_input(feats, backend, cols)
    y = feats["relation"].values
    groups = feats["seed"].values
    rows, cm, sizes = [], np.zeros((len(labels), len(labels)), int), []
    for rs in range(n_rep):
        gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=rs)
        tr, te = next(gss.split(feats, y, groups=groups))
        take = (lambda idx: X.iloc[idx]) if isinstance(X, pd.DataFrame) else (lambda idx: X[idx])
        kw = {"random_state": 42} if backend in {"gbm", "hgbm", "rf"} else {}
        est = _make_estimator(backend, cols, **kw)
        sw = compute_sample_weight("balanced", y[tr]) if backend in {"gbm", "hgbm"} else None
        fit_estimator(est, take(tr), y[tr], backend, sw)
        yp = est.predict(take(te))
        _, _, f, _ = precision_recall_fscore_support(y[te], yp, labels=labels, zero_division=0)
        rows.append({"macro_f1": f1_score(y[te], yp, labels=labels, average="macro", zero_division=0),
                     "weighted_f1": f1_score(y[te], yp, labels=labels, average="weighted", zero_division=0),
                     **{c: v for c, v in zip(labels, f)}})
        cm += confusion_matrix(y[te], yp, labels=labels)
        sizes.append(len(te))
    return pd.DataFrame(rows), cm, labels, len(cols), sizes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--annotations", required=True)
    ap.add_argument("--features", nargs="+", default=["lex", "lex_sbert"],
                    choices=["lex", "lex_sbert", "lex_svec"])
    ap.add_argument("--backends", nargs="+", default=["tfidf_logreg", "rf"],
                    choices=BACKENDS)
    ap.add_argument("--n-repeats", type=int, default=20)
    ap.add_argument("--test-size", type=float, default=0.25)
    ap.add_argument("--per-seed-cap", type=int, default=100, help="0 — без ограничения")
    ap.add_argument("--per-class-cap", type=int, default=300, help="0 — без ограничения")
    ap.add_argument("--exclude-relations", nargs="*", default=["associated_with"])
    ap.add_argument("--out", default="reports/repeated_eval.md")
    args = ap.parse_args()

    df = pd.read_csv(args.annotations, encoding="utf-8-sig")
    df = df.dropna(subset=["u_text", "v_text", "relation"])
    df = df[~df["relation"].isin(args.exclude_relations or [])]
    bal = balance(df, per_seed=args.per_seed_cap or None,
                  per_class=args.per_class_cap or None, random_state=42)

    lines = ["# Оценка на повторных групповых разбиениях\n",
             f"- пар после балансировки: **{len(bal)}**, групп (seed): **{bal['seed'].nunique()}**",
             f"- повторов: **{args.n_repeats}**, доля тестовых групп: {args.test_size}",
             f"- классы: {dict(bal['relation'].value_counts())}\n",
             "| Признаки | Алгоритм | Признаков | Macro-F1 | Weighted-F1 |",
             "|---|---|---:|---:|---:|"]
    details = []
    for mode in args.features:
        feats = build(bal, mode)
        for be in args.backends:
            R, cm, labels, n_cols, sizes = evaluate(feats, be, args.n_repeats, args.test_size)
            m, s = R["macro_f1"], R["weighted_f1"]
            row = f"| {mode} | {be} | {n_cols} | {m.mean():.3f} ± {m.std():.3f} | {s.mean():.3f} ± {s.std():.3f} |"
            lines.append(row)
            print(row, flush=True)
            details.append(f"\n## {mode} / {be}\n")
            details.append(f"Тестовых пар в повторе: от {min(sizes)} до {max(sizes)}\n")
            details.append("| Класс | F1 (среднее ± ст. откл.) |\n|---|---:|")
            for c in labels:
                details.append(f"| {c} | {R[c].mean():.3f} ± {R[c].std():.3f} |")
            details.append("\nСуммарная матрица ошибок (строки — истинный, столбцы — предсказанный):\n")
            details.append(pd.DataFrame(cm, index=labels, columns=labels).to_markdown())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines + details) + "\n", encoding="utf-8")
    print(f"\nОтчёт: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
