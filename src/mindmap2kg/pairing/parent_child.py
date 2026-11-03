"""
Выделение пар-кандидатов по стратегии "родитель → потомок".

Это базовая стратегия: каждое ребро ментальной карты превращается
в пару, направление сохраняется (от родителя к потомку).
"""
from __future__ import annotations

from ..core.base import BasePairing
from ..core.registry import register
from ..core.schemas import CandidatePair, MindMap


@register("pairing", "parent_child")
class ParentChildPairing(BasePairing):
    def extract(self, mm: MindMap) -> list[CandidatePair]:
        node_by_id = {n.id: n for n in mm.nodes}
        pairs: list[CandidatePair] = []
        for e in mm.edges:
            u = node_by_id[e.source]
            v = node_by_id[e.target]
            pairs.append(CandidatePair(
                pair_id=f"{u.id}__{v.id}",
                u_id=u.id, u_text=u.text,
                v_id=v.id, v_text=v.text,
            ))
        return pairs
