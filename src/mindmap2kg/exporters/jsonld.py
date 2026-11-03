"""
Экспорт KG в JSON-LD — для интеграции с веб-приложениями и semantic web.
Использует упрощённый контекст; в дальнейшем можно подключить нормальную онтологию
с правильными IRI и SKOS-мэппингами.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..core.base import BaseExporter
from ..core.registry import register
from ..core.schemas import KnowledgeGraph


@register("exporter", "jsonld")
class JsonLdExporter(BaseExporter):
    def __init__(self, base_iri: str = "https://mindmap2kg.org/v1/"):
        self.base_iri = base_iri

    def extension(self) -> str:
        return "jsonld"

    def export(self, kg: KnowledgeGraph, path: str | Path) -> None:
        doc = {
            "@context": {
                "@vocab": self.base_iri,
                "label": "http://www.w3.org/2000/01/rdf-schema#label",
            },
            "taxonomy_version": kg.taxonomy_version,
            "run_id": kg.run_id,
            "@graph": (
                [
                    {
                        "@id":   f"{self.base_iri}node/{n.id}",
                        "@type": "Concept",
                        "label": n.text,
                        "depth": n.depth,
                    }
                    for n in kg.nodes
                ]
                + [
                    {
                        "@id":        f"{self.base_iri}edge/{e.source}__{e.target}",
                        "@type":      "SemanticRelation",
                        "source":     f"{self.base_iri}node/{e.source}",
                        "target":     f"{self.base_iri}node/{e.target}",
                        "relation":   e.relation,
                        "confidence": e.confidence,
                    }
                    for e in kg.edges
                ]
            ),
        }
        Path(path).write_text(
            json.dumps(doc, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
