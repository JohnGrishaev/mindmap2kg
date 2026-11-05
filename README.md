# mindmap2kg

Преобразование ментальной карты (mind-map) в граф знаний с разметкой типов
семантических связей. ВКР 2026, кафедра «Прикладная информатика» Московского
Политеха.

## Установка

```bash
git clone <repo>
cd mindmap2kg
pip install -e .             # ядро
pip install -e ".[ui]"       # + Streamlit-дашборд и Plotly
pip install -e ".[all]"      # всё
```

## Быстрый старт (sanity check скелета)

```bash
# 1. Сгенерировать синтетические карты для тестирования
python scripts/generate_synthetic_maps.py

# 2. Прогнать пайплайн на одной из них (с dummy-классификатором)
python scripts/run_pipeline.py data/raw/synthetic_клетка.mm

# 3. Собрать обучающие данные из Wikidata (~10-15 минут на full seeds)
python scripts/extract_wikidata.py --seeds-set full
#   → data/labeled/annotations.csv

# 4. Сгенерировать precedes-пары из курируемого YAML (без LLM, мгновенно)
python scripts/seed_precedes.py
#   → data/labeled/precedes_pairs.csv

# 5. Склеить таблицы. ВАЖНО: precedes_pairs первым, чтобы не быть
#    вытесненным wikidata-парами при коллизиях.
python scripts/merge_annotations.py \
    data/labeled/precedes_pairs.csv \
    data/labeled/annotations.csv \
    --output data/labeled/annotations.csv

# 6. Аналитический отчёт по разметке
python scripts/analyze_annotations.py data/labeled/annotations.csv \
    --out reports/annotations_report.md

# 7. Обучить модель. --group-split: пары одного процесса/seed не попадают
#    одновременно в train и test. --refit-full: после оценки модель
#    переобучается на всех парах и сохраняется.
python scripts/train_classifier.py \
    --annotations data/labeled/annotations_v1.csv \
    --backend tfidf_logreg --run-id exp_tfidf \
    --per-seed-cap 100 --per-class-cap 300 \
    --group-split --refit-full --no-sbert
#   → models/exp_tfidf.joblib
#   → reports/exp_tfidf.md  + confusion.csv

# 7a. Оценка на 20 групповых разбиениях (среднее ± ст. откл.) — эти числа в ВКР
python scripts/evaluate_repeated.py \
    --annotations data/labeled/annotations_v1.csv \
    --features lex lex_sbert lex_svec --backends tfidf_logreg rf logreg

# 8. Запустить пайплайн с обученной моделью на карте
python scripts/run_pipeline.py data/raw/synthetic_клетка.mm \
    --config configs/experiments/exp_tfidf.yaml

# 9. Открыть UI (опционально)
streamlit run src/mindmap2kg/viz/dashboard.py
```

После п.2 в `data/interim/skeleton_demo/` появятся артефакты всех этапов:

```
01_graph.json        # распарсенный MindMap
02_pairs.csv         # извлечённые пары
03_features.csv      # пары + признаки
04_predictions.csv   # предсказания классификатора
kg.graphml           # итоговый KG для Gephi
kg.jsonld            # итоговый KG для веб-приложений
```

## Текущие результаты (20 групповых разбиений, без SBERT)

| Модель | Macro-F1 |
|---|---:|
| tfidf_logreg (символьные n-граммы меток + лексика) | 0.437 ± 0.056 |
| rf (только лексика) | 0.311 ± 0.042 |
| всегда has_example | 0.10 |

Важно: признаками считаются только колонки `lex_*`, `sbert_*`, `topo_*`.
До исправления в признаки попадала служебная колонка `curated_version`
(есть только у пар precedes) — это давало precedes F1 = 1.0 и ломало
применение модели к реальной карте. Модели в `models/exp_*_sbert.joblib`,
`exp_baseline_gbm.joblib` и отчёты к ним — старые (5 классов), их стоит
переобучить.

## Что уже работает

- **Парсер FreeMind** (`.mm`)
- **Выделение пар** «родитель → потомок»
- **Признаки:** простые лексические + топологические (NetworkX)
- **Заглушка-классификатор** для проверки скелета
- **Экспорт:** GraphML, JSON-LD

## Что предстоит (roadmap)

| Этап | Модуль | Статус |
|---|---|---|
| Sentence-BERT/RuBERT эмбеддинги | `features/text/sbert.py` | TODO |
| GBM / MLP классификаторы | `classifiers/sklearn_wrapper.py`, `mlp.py` | TODO |
| Sentence-BERT/RuBERT эмбеддинги | `features/text/sbert.py` | TODO |
| Сбор данных из Wikidata | `annotation/wikidata_extractor.py` | ✓ готово |
| LLM-разметка реальных карт | `annotation/llm_annotator.py` | TODO |
| Streamlit-аннотатор | `annotation/streamlit_app.py` | TODO |
| Полный дашборд (Compare Runs, Train, Annotate) | `viz/dashboard.py` | в работе |
| Внешние знания (Викисловарь) | `features/external/wiktionary.py` | TODO |

## Архитектура (вкратце)

```
.mm файл
   ↓ parser (FreeMind)
MindMap (dataclass)
   ↓ pairing (parent_child)
list[CandidatePair]
   ↓ feature extractors (lexical_simple, topology, ...)
DataFrame с признаками
   ↓ classifier (dummy → потом real)
list[Prediction]
   ↓ builder + exporters
KG (graphml, jsonld, ...)
```

Все компоненты — плагины, регистрируются через декоратор `@register("kind", "name")`.
Один YAML-конфиг описывает весь прогон. Артефакты каждого этапа сохраняются на диск.

Подробнее см. `configs/default.yaml`.

## Структура

```
src/mindmap2kg/
├── core/           # схемы, реестр, конфиг, оркестратор
├── parsers/        # .mm, .xmind, .json
├── pairing/        # стратегии выделения пар
├── features/       # text/, graph/, external/
├── classifiers/    # dummy, gbm, mlp, gnn
├── exporters/      # graphml, jsonld, ttl
├── annotation/     # сбор данных и разметка
└── viz/            # Streamlit, Plotly
```
