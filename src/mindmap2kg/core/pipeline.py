"""
Оркестратор пайплайна. Последовательно вызывает компоненты, указанные
в конфиге, и сохраняет артефакт после каждого этапа.

Поток данных:
    .mm файл
        → [parser]     MindMap        → 01_graph.json
        → [pairing]    list[Pair]     → 02_pairs.csv
        → [features]   DataFrame      → 03_features.csv
        → [classifier] list[Pred]     → 04_predictions.csv
        → [builder]    KnowledgeGraph
        → [exporters]                 → kg.{graphml,jsonld,...}
"""
from __future__ import annotations

import pandas as pd

from .artifacts import ArtifactStore
from .config import PipelineConfig
from .registry import get
from .schemas import CandidatePair, Edge, KnowledgeGraph, MindMap, Prediction


class Pipeline:
    def __init__(self, config: PipelineConfig, store: ArtifactStore, taxonomy: dict):
        self.config = config
        self.store = store
        self.taxonomy = taxonomy

    def run(self, input_file: str) -> KnowledgeGraph:
        # --- 1. Парсинг ---
        Parser = get("parser", self.config.parser.name)
        mm = Parser(**self.config.parser.options).parse(input_file)
        self.store.save_mindmap(mm, "01_graph")
        print(f"  [01 parse]      узлов: {len(mm.nodes)}, рёбер: {len(mm.edges)}")

        # --- 2. Выделение пар ---
        Pairing = get("pairing", self.config.pairing.name)
        pairs: list[CandidatePair] = Pairing(**self.config.pairing.options).extract(mm)
        pairs_df = pd.DataFrame([p.__dict__ for p in pairs])
        self.store.save_table(pairs_df, "02_pairs")
        print(f"  [02 pairing]    пар-кандидатов: {len(pairs)}")

        # --- 3. Признаки ---
        features_df = pairs_df.copy()
        cols_before = set(features_df.columns)
        for fspec in self.config.features:
            FeatCls = get("feature", fspec.name)
            features_df = FeatCls(**fspec.options).transform(features_df, mm)
        new_cols = sorted(set(features_df.columns) - cols_before)
        self.store.save_table(features_df, "03_features")
        print(f"  [03 features]   новых признаков: {len(new_cols)}  ({', '.join(new_cols[:6])}{'...' if len(new_cols) > 6 else ''})")

        # --- 4. Классификация ---
        ClfCls = get("classifier", self.config.classifier.name)
        clf = ClfCls(taxonomy=self.taxonomy, **self.config.classifier.options)
        predictions: list[Prediction] = clf.predict(features_df)
        preds_df = pd.DataFrame([p.__dict__ for p in predictions])
        self.store.save_table(preds_df, "04_predictions")
        from collections import Counter
        dist = Counter(p.relation for p in predictions)
        print(f"  [04 classify]   предсказаний: {len(predictions)}  "
              f"({', '.join(f'{k}={v}' for k, v in dist.most_common(3))}...)")

        # --- 5. Сборка KG ---
        pred_by_pair = {p.pair_id: p for p in predictions}
        kg_edges = []
        for e in mm.edges:
            pid = f"{e.source}__{e.target}"
            pred = pred_by_pair.get(pid)
            kg_edges.append(Edge(
                source=e.source,
                target=e.target,
                relation=pred.relation if pred else None,
                confidence=pred.confidence if pred else None,
            ))
        kg = KnowledgeGraph(
            nodes=mm.nodes,
            edges=kg_edges,
            taxonomy_version=self.taxonomy.get("version", "unknown"),
            run_id=self.config.run_id,
        )

        # --- 6. Экспорт ---
        for exp_spec in self.config.exporters:
            ExpCls = get("exporter", exp_spec.name)
            exporter = ExpCls(**exp_spec.options)
            out = self.store.path(f"kg.{exporter.extension()}")
            exporter.export(kg, out)
            print(f"  [05 export]     {exporter.extension()}: {out.name}")

        print(f"\n  Все артефакты в: {self.store.base}")
        return kg
