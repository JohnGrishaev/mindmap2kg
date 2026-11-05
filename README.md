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
    --config configs/experiments/exp_maps.yaml

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

## Текущие результаты

| Модель | Обучающие данные | Macro-F1 | Синтетические карты |
|---|---|---:|---:|
| **exp_maps**: tfidf_logreg + топология | 86 размеченных карт (`maps_llm.csv`) | **0.641 ± 0.038** (на незнакомых картах) | 45/56 |
| exp_tfidf_sbert: tfidf_logreg + SBERT-векторы | Wikidata (`annotations_v1.csv`) | 0.496 ± 0.043 | 31/56 |
| exp_tfidf: tfidf_logreg | Wikidata | 0.437 ± 0.056 | 28/56 |
| rf, только лексика | Wikidata | 0.311 ± 0.042 | 21/56 |

Macro-F1 — среднее по 20 групповым разбиениям (`scripts/evaluate_repeated.py`).
Модель на Wikidata, применённая к картам, даёт лишь 0.29: пары из Wikidata
выглядят не так, как связи в картах, и не имеют дерева. Обучение на картах
решает обе проблемы и включает признаки топологии (+0.08).

Карты в `data/generated/` сгенерированы языковой моделью (Claude) по темам
школьного/вузовского курса биологии и размечены ею же; исходные схемы —
`data/generated/outlines/*.txt`. Окончательная проверка — на настоящих
картах (`scripts/labeling.py`, см. ниже).

Важно: признаками считаются только колонки `lex_*`, `sbert_*`, `topo_*`.
До исправления в признаки попадала служебная колонка `curated_version`
(есть только у пар precedes) — это давало precedes F1 = 1.0 и ломало
применение модели к реальной карте.

## Размеченные карты

```bash
# Схемы → .mm с атрибутом GOLD_RELATION → таблица пар с топологией
python scripts/outline_to_mm.py data/generated/outlines/*.txt --out-dir data/generated/maps
python scripts/extract_labeled_pairs.py data/generated/maps --output data/labeled/maps_llm.csv

# Обучение рабочей модели
python scripts/train_classifier.py --annotations data/labeled/maps_llm.csv \
    --backend tfidf_logreg --no-sbert --per-seed-cap 0 --per-class-cap 0 \
    --run-id exp_maps --group-split --refit-full

# Настоящие карты: выгрузка в Excel для разметки и обратно
python scripts/labeling.py export data/real/maps --output data/real/to_label.xlsx
python scripts/labeling.py apply data/real/to_label.xlsx \
    --maps-dir data/real/maps --out-dir data/real/labeled_maps
```

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
