"""
Streamlit-дашборд (минимальный скелет).

Запуск:
    pip install -e ".[ui]"
    streamlit run src/mindmap2kg/viz/dashboard.py

На данный момент реализована только вкладка Upload & Run. Следующие шаги:
  - Annotate (ручная разметка пар через UI)
  - Train (обучение классификатора на размеченных данных)
  - Compare Runs (сравнение метрик нескольких прогонов)
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

import mindmap2kg  # noqa: F401 — регистрирует плагины
from mindmap2kg.core.artifacts import ArtifactStore
from mindmap2kg.core.config import load_config, load_taxonomy
from mindmap2kg.core.pipeline import Pipeline


st.set_page_config(page_title="mindmap2kg", layout="wide")
st.title("mindmap2kg — преобразование mind-map в граф знаний")

tabs = st.tabs(["📤 Upload & Run", "🏷️ Annotate", "🧪 Train", "📊 Compare Runs"])

# ---------------------------------------------------------------------------
# Tab 1: Upload & Run
# ---------------------------------------------------------------------------
with tabs[0]:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Параметры")
        config_path = st.text_input("Конфиг", value="configs/experiments/exp_baseline_gbm.yaml") # upd default
        uploaded = st.file_uploader("Загрузить mind-map (.mm)", type=["mm"])
        run_btn = st.button("Запустить пайплайн", disabled=(uploaded is None))

    with col2:
        st.subheader("Результат")

        if run_btn and uploaded is not None:
            # сохраняем загруженный файл во временное место
            with tempfile.NamedTemporaryFile(suffix=".mm", delete=False) as f:
                f.write(uploaded.read())
                tmp_path = f.name

            config = load_config(config_path)
            taxonomy = load_taxonomy(config.taxonomy)
            store = ArtifactStore("data/interim", config.run_id)
            pipeline = Pipeline(config, store, taxonomy)

            with st.spinner("Прогон пайплайна..."):
                kg = pipeline.run(tmp_path)

            st.success(f"Готово. {len(kg.nodes)} узлов, {len(kg.edges)} рёбер.")

            # Распределение типов связей
            rel_dist = pd.Series([e.relation for e in kg.edges]).value_counts()
            st.bar_chart(rel_dist)

            # Таблица рёбер
            edges_df = pd.DataFrame([
                {
                    "source": next(n.text for n in kg.nodes if n.id == e.source),
                    "target": next(n.text for n in kg.nodes if n.id == e.target),
                    "relation": e.relation,
                    "confidence": e.confidence,
                }
                for e in kg.edges
            ])
            st.dataframe(edges_df, use_container_width=True)

            Path(tmp_path).unlink(missing_ok=True)

# ---------------------------------------------------------------------------
# Tab 2-4: заглушки
# ---------------------------------------------------------------------------
with tabs[1]:
    st.info("TODO: интерфейс ручной разметки пар (annotation/streamlit_app.py).")
with tabs[2]:
    st.info("TODO: обучение классификатора на data/labeled/.")
with tabs[3]:
    st.info("TODO: сравнение метрик нескольких run_id.")
