"""
Структурно-графовые признаки пары узлов.

Используем NetworkX как удобный API для вычислений по графу.
"""
from __future__ import annotations

import networkx as nx
import pandas as pd

from ...core.base import BaseFeature
from ...core.registry import register
from ...core.schemas import MindMap


@register("feature", "topology")
class TopologyFeatures(BaseFeature):
    def transform(self, df: pd.DataFrame, mm: MindMap) -> pd.DataFrame:
        # Строим nx.DiGraph один раз
        G = nx.DiGraph()
        for n in mm.nodes:
            G.add_node(n.id, depth=n.depth, text=n.text)
        for e in mm.edges:
            G.add_edge(e.source, e.target)

        # Для расчёта расстояния и НОА строим также неориентированную версию
        # (mind-map по сути дерево, поэтому НОА однозначен)
        UG = G.to_undirected()

        df = df.copy()
        df["topo_depth_u"]      = df["u_id"].map(lambda i: G.nodes[i]["depth"])
        df["topo_depth_v"]      = df["v_id"].map(lambda i: G.nodes[i]["depth"])
        df["topo_depth_diff"]   = df["topo_depth_v"] - df["topo_depth_u"]
        df["topo_outdeg_u"]     = df["u_id"].map(lambda i: G.out_degree(i))
        df["topo_outdeg_v"]     = df["v_id"].map(lambda i: G.out_degree(i))
        df["topo_indeg_u"]      = df["u_id"].map(lambda i: G.in_degree(i))
        df["topo_indeg_v"]      = df["v_id"].map(lambda i: G.in_degree(i))
        df["topo_v_is_leaf"]    = df["topo_outdeg_v"] == 0
        df["topo_u_branching"]  = df["topo_outdeg_u"]   # сколько потомков у родителя
        # Сиблинги: сколько у u есть детей кроме v
        df["topo_v_siblings"]   = df["topo_outdeg_u"] - 1

        return df
