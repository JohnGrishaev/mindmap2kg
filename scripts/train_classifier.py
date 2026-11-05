"""
Обучение и оценка классификатора типов связей на размеченных парах.

Поток:
  1. читаем data/labeled/annotations.csv
  2. (опц.) балансируем (cap-per-seed / cap-per-class) → отдельная таблица
  3. строим признаки: lexical_simple + sbert (с --sbert-vectors — полные векторы)
     [топология не считается — для табличных пар у нас нет MindMap;
      она доступна только в инференсе на реальной карте]
  4. train/test split: групповой по seed (--group-split) или стратифицированный
  5. обучаем модель (tfidf_logreg/gbm/logreg/rf/hgbm)
  6. метрики: macro-F1, per-class precision/recall/F1, confusion matrix
  7. сохраняем модель → models/{run_id}.joblib
  8. сохраняем отчёт → reports/{run_id}.md и confusion.csv

Использование:
    python scripts/train_classifier.py \\
        --annotations data/labeled/annotations.csv \\
        --backend tfidf_logreg \\
        --run-id exp_tfidf \\
        --per-class-cap 300 --per-seed-cap 100 --group-split

Замечание про topology-фичи:
  В этом скрипте мы обучаемся на табличных парах (без mind-map). Топология
  не вычисляется. На инференсе в пайплайне (где есть MindMap) топология
  будет, но классификатор обучен без неё → значит, в пайплайне нужно
  использовать ТОТ ЖЕ список feature_columns (он сохраняется в .joblib).
  Если хочешь включить топологию в обучение — синтезируй искусственные
  mind-map'ы из аннотаций (scripts/generate_synthetic_maps.py — задел уже есть).
"""
from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# Регистрируем плагины
import mindmap2kg  # noqa: F401
from mindmap2kg.annotation.balance import balance
from mindmap2kg.classifiers.sklearn_wrapper import (
    BACKENDS, SklearnClassifier, make_input, select_feature_columns,
)
from mindmap2kg.core.schemas import MindMap, Node
from mindmap2kg.core.registry import get

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s :: %(message)s")


def make_stub_mindmap(df: pd.DataFrame) -> MindMap:
    """
    Заглушка MindMap, чтобы фичеры с интерфейсом transform(df, mm) могли
    отработать без реальной карты. Лексические/SBERT фичи не используют mm.
    Топология НЕ применяется в этом режиме (см. docstring модуля).
    """
    nodes = [Node(id=f"u_{i}", text="") for i in range(len(df))]
    return MindMap(nodes=nodes, edges=[], root_id="u_0",
                   source_file="<stub>", source_format="stub")


def build_features(df: pd.DataFrame,
                   use_sbert: bool = True,
                   sbert_model: str | None = None,
                   sbert_vectors: bool = False) -> pd.DataFrame:
    """Применяет фичеры: lexical_simple (+sbert опционально)."""
    # pair_id, u_id, v_id — нужны контрактом фичеров. Подмешиваем.
    work = df.copy()
    if "pair_id" not in work.columns:
        work["pair_id"] = [f"p_{i}" for i in range(len(work))]
    if "u_id" not in work.columns:
        work["u_id"] = work["pair_id"] + "_u"
    if "v_id" not in work.columns:
        work["v_id"] = work["pair_id"] + "_v"

    mm = make_stub_mindmap(work)

    LexCls = get("feature", "lexical_simple")
    work = LexCls().transform(work, mm)
    logger.info("После lexical_simple: %d колонок", work.shape[1])

    if use_sbert:
        SBertCls = get("feature", "sbert")
        sbert_kwargs = {"include_vectors": sbert_vectors}
        if sbert_model:
            sbert_kwargs["model_name"] = sbert_model
        work = SBertCls(**sbert_kwargs).transform(work, mm)
        logger.info("После SBERT: %d колонок", work.shape[1])

    return work


def report_metrics(y_true, y_pred, classes: list[str]) -> dict:
    from sklearn.metrics import (classification_report, confusion_matrix,
                                 f1_score, precision_recall_fscore_support)
    macro_f1 = f1_score(y_true, y_pred, average="macro", labels=classes, zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average="weighted", labels=classes, zero_division=0)
    report_dict = classification_report(y_true, y_pred, labels=classes,
                                        output_dict=True, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    return {
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "report": report_dict,
        "confusion": cm,
        "labels": classes,
    }


def format_report_md(run_id: str, args, train_size: int, test_size: int,
                     class_dist: dict, metrics: dict,
                     feature_columns: list[str]) -> str:
    lines = []
    P = lines.append
    P(f"# Отчёт об обучении: `{run_id}`\n")
    P(f"- backend: **{args.backend}**")
    P(f"- per-seed cap: {args.per_seed_cap}")
    P(f"- per-class cap: {args.per_class_cap}")
    P(f"- test size: {args.test_size}")
    P(f"- use SBERT: {not args.no_sbert}, full vectors: {args.sbert_vectors}")
    P(f"- random state: {args.random_state}")
    P(f"- train pairs: **{train_size}**, test pairs: **{test_size}**")
    P(f"- признаков: **{len(feature_columns)}**")
    P("")

    P("## Распределение классов в обучении\n")
    P(pd.Series(class_dist).to_frame("count").to_markdown())
    P("")

    P("## Метрики\n")
    P(f"- macro-F1:    **{metrics['macro_f1']:.4f}**")
    P(f"- weighted-F1: **{metrics['weighted_f1']:.4f}**")
    P("")

    P("### Per-class\n")
    rep = metrics["report"]
    rows = []
    for cls in metrics["labels"]:
        if cls in rep:
            rows.append({
                "class":    cls,
                "precision": round(rep[cls]["precision"], 4),
                "recall":    round(rep[cls]["recall"], 4),
                "f1":        round(rep[cls]["f1-score"], 4),
                "support":   int(rep[cls]["support"]),
            })
    P(pd.DataFrame(rows).to_markdown(index=False))
    P("")

    P("### Confusion matrix (строки — true, столбцы — pred)\n")
    cm_df = pd.DataFrame(metrics["confusion"],
                         index=metrics["labels"], columns=metrics["labels"])
    P(cm_df.to_markdown())
    P("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--annotations", required=True, nargs="+",
                    help="CSV с парами и колонкой relation (можно несколько — склеиваются)")
    ap.add_argument("--exclude-relations", nargs="*", default=["associated_with"],
                    help="Классы, которые не участвуют в обучении (по умолчанию "
                         "резервный associated_with)")
    ap.add_argument("--backend", default="tfidf_logreg", choices=BACKENDS)
    ap.add_argument("--run-id", default="baseline_gbm",
                    help="Идентификатор прогона (для имён файлов)")
    ap.add_argument("--per-seed-cap", type=int, default=100,
                    help="Не больше N пар на один seed/карту; 0 — без ограничения")
    ap.add_argument("--per-class-cap", type=int, default=300,
                    help="Не больше N пар на класс; 0 — без ограничения")
    ap.add_argument("--test-size", type=float, default=0.25)
    ap.add_argument("--random-state", type=int, default=42)
    ap.add_argument("--group-split", action="store_true",
                    help="Группированный split: пары из одного seed целиком "
                         "идут либо в train, либо в test. Даёт честную "
                         "оценку генерализации на новый процесс/тему. "
                         "Особенно важно для precedes (этапы одного процесса "
                         "не должны попасть и в train, и в test).")
    ap.add_argument("--refit-full", action="store_true",
                    help="После оценки переобучить модель на всех парах и "
                         "сохранить её (метрики в отчёте — по тестовой части).")
    ap.add_argument("--sbert-vectors", action="store_true",
                    help="Передавать в модель полные SBERT-векторы u, v, u−v, u⊙v "
                         "(1536 признаков). Рекомендуется с --backend tfidf_logreg.")
    ap.add_argument("--no-sbert", action="store_true",
                    help="Без SBERT (только лексика). Для smoke-теста.")
    ap.add_argument("--sbert-model", default=None,
                    help="Имя модели sentence-transformers")
    ap.add_argument("--models-dir", default="models")
    ap.add_argument("--reports-dir", default="reports")
    ap.add_argument("--taxonomy", default="configs/taxonomy.yaml")
    args = ap.parse_args()

    # --- 1. Загрузка ---------------------------------------------------------
    df = pd.concat([pd.read_csv(p, encoding="utf-8-sig") for p in args.annotations],
                   ignore_index=True)
    logger.info("Загружено пар: %d из %d файлов", len(df), len(args.annotations))
    if "relation" not in df.columns:
        raise ValueError("В таблице нет колонки 'relation'")

    # Чистка: пустые u_text/v_text/relation
    n_before = len(df)
    df = df.dropna(subset=["u_text", "v_text", "relation"])
    df = df[(df["u_text"].astype(str).str.strip() != "") &
            (df["v_text"].astype(str).str.strip() != "")]
    if len(df) != n_before:
        logger.warning("Удалено строк с пустыми текстами/relation: %d",
                       n_before - len(df))

    if args.exclude_relations:
        n0 = len(df)
        df = df[~df["relation"].isin(args.exclude_relations)]
        logger.info("Исключено пар классов %s: %d", args.exclude_relations, n0 - len(df))

    # --- 2. Балансировка ----------------------------------------------------
    df_bal = balance(df,
                     per_seed=args.per_seed_cap or None,
                     per_class=args.per_class_cap or None,
                     drop_collisions_flag=True,
                     random_state=args.random_state)
    logger.info("После балансировки: %d пар", len(df_bal))
    dist_after = dict(Counter(df_bal["relation"]))
    logger.info("Распределение: %s", dist_after)

    # Хватает ли данных?
    too_small = {c: n for c, n in dist_after.items() if n < 10}
    if too_small:
        logger.warning("Классы с <10 примеров: %s — будут плохо обучаться",
                       too_small)

    # --- 3. Признаки --------------------------------------------------------
    feats = build_features(df_bal,
                           use_sbert=not args.no_sbert,
                           sbert_model=args.sbert_model,
                           sbert_vectors=args.sbert_vectors)
    feature_columns = select_feature_columns(feats)
    logger.info("Признаков для модели: %d", len(feature_columns))

    # Защита от NaN в числовых признаках (GBM их не принимает).
    # Источники NaN: пустые токены в Jaccard, отсутствующие узлы и т.п.
    n_nan = feats[feature_columns].isna().sum().sum()
    if n_nan:
        logger.warning("NaN в признаках: %d значений → заполняю нулями", n_nan)
        feats[feature_columns] = feats[feature_columns].fillna(0)

    # --- 4. Train/test split ------------------------------------------------
    if args.group_split:
        if "seed" not in feats.columns:
            raise ValueError("--group-split требует колонки 'seed' в данных")
        from sklearn.model_selection import GroupShuffleSplit
        gss = GroupShuffleSplit(n_splits=1, test_size=args.test_size,
                                random_state=args.random_state)
        train_idx, test_idx = next(gss.split(feats, feats["relation"],
                                              groups=feats["seed"]))
        X_train, X_test = feats.iloc[train_idx], feats.iloc[test_idx]
        y_train, y_test = X_train["relation"], X_test["relation"]
        train_seeds = set(X_train["seed"].unique())
        test_seeds = set(X_test["seed"].unique())
        logger.info("Group split: train seeds=%d, test seeds=%d, "
                    "overlap=%d (должно быть 0)",
                    len(train_seeds), len(test_seeds),
                    len(train_seeds & test_seeds))
    else:
        from sklearn.model_selection import train_test_split

        # Стратифицируем только если в каждом классе >=2 примеров
        rel_counts = Counter(feats["relation"])
        stratify = feats["relation"] if all(c >= 2 for c in rel_counts.values()) else None

        X_train, X_test, y_train, y_test = train_test_split(
            feats, feats["relation"],
            test_size=args.test_size,
            random_state=args.random_state,
            stratify=stratify,
        )
    logger.info("Train: %d, Test: %d", len(X_train), len(X_test))

    # --- 5. Загрузка таксономии и обучение ---------------------------------
    taxonomy = yaml.safe_load(Path(args.taxonomy).read_text(encoding="utf-8"))

    # Дисбаланс: rf/logreg/tfidf_logreg — class_weight="balanced" (по умолчанию
    # в _make_estimator); у GradientBoosting class_weight нет — даём sample_weight.
    extra_kw: dict = {}
    if args.backend in {"gbm", "hgbm", "rf"}:
        extra_kw["random_state"] = args.random_state
    sample_weight = None
    if args.backend in {"gbm", "hgbm"}:
        from sklearn.utils.class_weight import compute_sample_weight
        sample_weight = compute_sample_weight("balanced", y_train)

    clf = SklearnClassifier(taxonomy=taxonomy, backend=args.backend, **extra_kw)
    clf.fit(X_train, y_train, feature_columns=feature_columns,
            sample_weight=sample_weight)
    est = clf.estimator

    # --- 6. Оценка ----------------------------------------------------------
    Xte = make_input(X_test, args.backend, feature_columns)
    y_pred = est.predict(Xte)

    all_labels = sorted(set(y_train.tolist() + y_test.tolist()))
    metrics = report_metrics(y_test.values, y_pred, all_labels)

    print("\n" + "="*60)
    print(f"  macro-F1:    {metrics['macro_f1']:.4f}")
    print(f"  weighted-F1: {metrics['weighted_f1']:.4f}")
    print("="*60)
    rep = metrics["report"]
    print(f"{'class':<18} {'P':>7} {'R':>7} {'F1':>7} {'N':>5}")
    for cls in all_labels:
        if cls in rep:
            r = rep[cls]
            print(f"{cls:<18} {r['precision']:>7.3f} {r['recall']:>7.3f} "
                  f"{r['f1-score']:>7.3f} {int(r['support']):>5d}")

    # --- 7. Сохранение модели ----------------------------------------------
    if args.refit_full:
        sw_all = None
        if args.backend in {"gbm", "hgbm"}:
            from sklearn.utils.class_weight import compute_sample_weight
            sw_all = compute_sample_weight("balanced", feats["relation"])
        clf.fit(feats, feats["relation"], feature_columns=feature_columns,
                sample_weight=sw_all)
        logger.info("Модель переобучена на всех %d парах", len(feats))
    models_dir = Path(args.models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / f"{args.run_id}.joblib"
    clf.save(model_path)

    # --- 8. Отчёт -----------------------------------------------------------
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    md = format_report_md(args.run_id, args, len(X_train), len(X_test),
                          dist_after, metrics, feature_columns)
    (reports_dir / f"{args.run_id}.md").write_text(md, encoding="utf-8")

    cm_df = pd.DataFrame(metrics["confusion"],
                         index=metrics["labels"], columns=metrics["labels"])
    cm_df.to_csv(reports_dir / f"{args.run_id}_confusion.csv")

    logger.info("Отчёт: %s", reports_dir / f"{args.run_id}.md")
    logger.info("Модель: %s", model_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
