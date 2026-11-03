"""
Контракты данных, передаваемые между этапами пайплайна.

Используем stdlib dataclasses вместо pydantic — меньше зависимостей,
проще для старта. Если позже понадобится строгая валидация (например,
загрузка артефактов из ненадёжных источников), мигрируем точечно.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import json
from pathlib import Path


@dataclass
class Node:
    """Узел ментальной карты."""
    id: str
    text: str
    depth: int = 0
    text_normalized: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """Ребро. На этапе парсинга relation=None, заполняется классификатором."""
    source: str
    target: str
    relation: str | None = None
    confidence: float | None = None


@dataclass
class MindMap:
    """Внутреннее представление ментальной карты после парсинга."""
    nodes: list[Node]
    edges: list[Edge]
    root_id: str
    source_file: str
    source_format: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "nodes":         [asdict(n) for n in self.nodes],
            "edges":         [asdict(e) for e in self.edges],
            "root_id":       self.root_id,
            "source_file":   self.source_file,
            "source_format": self.source_format,
            "metadata":      self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> MindMap:
        return cls(
            nodes=[Node(**n) for n in d["nodes"]],
            edges=[Edge(**e) for e in d["edges"]],
            root_id=d["root_id"],
            source_file=d["source_file"],
            source_format=d["source_format"],
            metadata=d.get("metadata", {}),
        )

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> MindMap:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass
class CandidatePair:
    """Пара узлов-кандидатов для классификации."""
    pair_id: str
    u_id: str
    u_text: str
    v_id: str
    v_text: str


@dataclass
class Prediction:
    """Результат классификации одной пары."""
    pair_id: str
    relation: str
    confidence: float
    all_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class KnowledgeGraph:
    """Итоговый размеченный граф знаний."""
    nodes: list[Node]
    edges: list[Edge]            # все edges имеют relation
    taxonomy_version: str
    run_id: str

    def to_dict(self) -> dict:
        return {
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "taxonomy_version": self.taxonomy_version,
            "run_id": self.run_id,
        }
