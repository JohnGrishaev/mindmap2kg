# Техническая документация — mindmap2kg

## Что делает система

Принимает файл ментальной карты формата FreeMind (`.mm`), определяет тип смысловой связи между каждой парой понятий и возвращает граф знаний с подписанными стрелками.

---

## Быстрый старт

### Установка зависимостей

```bash
pip install -e ".[text,ml,ui]"
```

### Запуск веб-интерфейса

```bash
streamlit run src/mindmap2kg/viz/dashboard.py
```

Откроется браузер. Загружаешь `.mm` файл — получаешь таблицу пар и граф.

---

## Структура проекта

```
mindmap2kg/
│
├── src/mindmap2kg/
│   ├── core/               # ядро: схемы данных, реестр плагинов, оркестратор
│   │   ├── schemas.py      # dataclass-контракты: MindMap, KnowledgeGraph, Edge
│   │   ├── registry.py     # декоратор @register и функция get_plugin()
│   │   ├── pipeline.py     # оркестратор — запускает шаги по порядку
│   │   └── config.py       # чтение YAML-конфига
│   │
│   ├── parsers/
│   │   └── freemind.py     # читает .mm файл → объект MindMap
│   │
│   ├── pairing/
│   │   └── parent_child.py # обходит дерево → список пар (родитель, потомок)
│   │
│   ├── features/
│   │   ├── text/
│   │   │   ├── lexical_simple.py  # схожесть по буквам и словам
│   │   │   └── sbert.py           # смысловые признаки через нейросеть
│   │   └── graph/
│   │       └── topology.py        # глубина узла, число соседей, число потомков
│   │
│   ├── classifiers/
│   │   ├── sklearn_wrapper.py     # обёртка над scikit-learn (GBM / RF / LogReg)
│   │   └── dummy.py               # заглушка для тестирования без модели
│   │
│   ├── annotation/
│   │   ├── balance.py             # балансировка классов перед обучением
│   │   └── wikidata_extractor.py  # SPARQL-запросы к Викидате
│   │
│   ├── exporters/
│   │   ├── graphml_exp.py         # сохраняет граф в .graphml (для Gephi)
│   │   └── jsonld.py              # сохраняет граф в .json (семантический формат)
│   │
│   └── viz/
│       └── dashboard.py           # веб-интерфейс на Streamlit
│
├── scripts/
│   ├── extract_wikidata.py        # скачивает обучающие пары из Викидаты
│   ├── seed_precedes.py           # генерирует пары «предшествует» из YAML
│   ├── merge_annotations.py       # объединяет несколько источников данных
│   ├── train_classifier.py        # обучает модель и сохраняет отчёт
│   ├── compare_runs.py            # сравнивает результаты нескольких обучений
│   └── run_pipeline.py            # запускает пайплайн без интерфейса (CLI)
│
├── configs/
│   ├── taxonomy.yaml              # список типов связей
│   ├── biology_sequences.yaml     # вручную написанные цепочки этапов
│   ├── default.yaml               # конфиг с заглушкой (для проверки)
│   └── experiments/
│       └── exp_baseline_gbm.yaml  # конфиг с реальной обученной моделью
│
├── data/
│   ├── labeled/
│   │   └── annotations.csv        # 2018 размеченных пар — обучающий датасет
│   └── cache/sbert/               # кэш числовых представлений слов
│
├── models/
│   └── exp_baseline_gbm.joblib    # сохранённая обученная модель
│
├── reports/
│   ├── exp_rf_sbert.md            # отчёт по Random Forest
│   ├── exp_gbm_sbert.md           # отчёт по GBM
│   ├── exp_logreg_sbert.md        # отчёт по логистической регрессии
│   └── comparison.md              # сводная таблица всех трёх
│
└── pyproject.toml                 # список зависимостей, установка через pip
```

---

## Как работает программа шаг за шагом

```
.mm файл
    ↓
parsers/freemind.py       — читает XML-структуру карты
    ↓
pairing/parent_child.py   — достаёт все пары (родитель → потомок)
    ↓
features/                 — считает 10 признаков для каждой пары
    ↓
classifiers/              — загружает models/*.joblib, предсказывает тип связи
    ↓
exporters/                — сохраняет граф в .graphml и .json
    ↓
viz/dashboard.py          — показывает таблицу и график в браузере
```

---

## Типы связей (taxonomy.yaml)

| Идентификатор | Смысл | Пример |
|---|---|---|
| `has_part` | Часть целого | Клетка → Митохондрия |
| `has_example` | Пример / подвид | Млекопитающее → Кошка |
| `has_property` | Характеристика | Вода → Прозрачность |
| `has_function` | Функция | Митохондрия → Синтез АТФ |
| `causes` | Причина → следствие | Вирус → Заболевание |
| `precedes` | Предшествует | Профаза → Метафаза |

---

## Признаки пары слов

Для каждой пары вычисляется 10 чисел, которые передаются в модель.

**Лексические** (`features/text/lexical_simple.py`):
- `jaccard_char` — схожесть по парам букв
- `jaccard_word` — схожесть по словам
- `common_prefix_len` — длина общего начала
- `len_ratio` — отношение длин строк

**Топологические** (`features/graph/topology.py`):
- `depth_child` — глубина дочернего узла в дереве
- `n_siblings` — число узлов-соседей
- `n_children_child` — число потомков дочернего узла

**Смысловые** (`features/text/sbert.py`):
- `sbert_cos` — угол между смысловыми векторами
- `sbert_l2` — расстояние между смысловыми векторами
- `sbert_dot` — скалярное произведение векторов

Смысловые векторы вычисляет нейросеть `paraphrase-multilingual-MiniLM-L12-v2` (~120 МБ, скачивается один раз, работает офлайн, поддерживает русский и английский).

---

## Обучение модели

### Подготовка данных

```bash
# 1. Скачать пары из Викидаты
python scripts/extract_wikidata.py --seeds-set full

# 2. Сгенерировать пары «предшествует» из YAML
python scripts/seed_precedes.py

# 3. Объединить источники
python scripts/merge_annotations.py \
    data/labeled/precedes_pairs.csv \
    data/labeled/wikidata.csv \
    --output data/labeled/annotations.csv
```

### Обучение

```bash
python scripts/train_classifier.py \
    --annotations data/labeled/annotations.csv \
    --backend gbm \
    --run-id exp_baseline_gbm \
    --per-seed-cap 100 \
    --per-class-cap 300 \
    --group-split
```

Параметры:
- `--backend` — алгоритм: `gbm`, `rf` или `logreg`
- `--per-seed-cap 100` — не более 100 пар от одного термина
- `--per-class-cap 300` — не более 300 пар на класс
- `--group-split` — честное разделение: все пары одного термина идут только в обучение или только в проверку

После обучения появятся:
- `models/exp_baseline_gbm.joblib` — сохранённая модель
- `reports/exp_baseline_gbm.md` — отчёт с метриками

### Сравнение нескольких обучений

```bash
python scripts/compare_runs.py reports/exp_*.md --output reports/comparison.md
```

---

## Результаты обучения

| Алгоритм | Правильных ответов (macro) | Правильных ответов (weighted) |
|---|---|---|
| Random Forest | 40,7 % | 48,5 % |
| GBM | 38,3 % | 45,3 % |
| Логистическая регрессия | 22,8 % | 20,9 % |

Класс `precedes` распознаётся с точностью 100%. Слабые места — классы `has_function` и `has_part`: мало обучающих примеров.

---

## Просмотр графа в Gephi

1. Открыть Gephi → File → Open → выбрать `.graphml` из `data/interim/`
2. Вкладка **Edges** внизу → колонка `relation` — там типы связей
3. **View → Show Edge Labels** — подписи на стрелках
4. **Appearance → Edges → Unique color → relation** — раскраска по типу

---

## Конфигурационные файлы

| Файл | Назначение |
|---|---|
| `configs/taxonomy.yaml` | Список типов связей |
| `configs/biology_sequences.yaml` | Ручные цепочки для класса `precedes` |
| `configs/default.yaml` | Запуск с заглушкой (для проверки без модели) |
| `configs/experiments/exp_baseline_gbm.yaml` | Запуск с реальной обученной моделью |

---

## Зависимости

```toml
# Базовые (устанавливаются всегда)
pyyaml, networkx, pandas, lxml, click, requests

# Текст и смысловые признаки
pip install -e ".[text]"    # sentence-transformers, spacy

# Классификаторы
pip install -e ".[ml]"      # scikit-learn, torch

# Интерфейс
pip install -e ".[ui]"      # streamlit, plotly

# Всё сразу
pip install -e ".[text,ml,ui]"
```
