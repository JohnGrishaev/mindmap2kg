"""
Экспорт KG в формат GraphML — для анализа в Gephi и других графовых редакторах.
"""
from __future__ import annotations

from pathlib import Path
import networkx as nx

from ..core.base import BaseExporter
from ..core.registry import register
from ..core.schemas import KnowledgeGraph


@register("exporter", "graphml")
class GraphMLExporter(BaseExporter):
    def extension(self) -> str:
        return "graphml"

    def export(self, kg: KnowledgeGraph, path: str | Path) -> None:
        G = nx.DiGraph()
        for n in kg.nodes:
            G.add_node(n.id, label=n.text, depth=int(n.depth))
        for e in kg.edges:
            G.add_edge(
                e.source, e.target,
                relation=e.relation or "unknown",
                confidence=float(e.confidence) if e.confidence is not None else 0.0,
            )
        nx.write_graphml(G, str(path), encoding="utf-8")
