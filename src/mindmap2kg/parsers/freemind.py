"""
Парсер формата FreeMind (.mm). Структура:
    <map version="...">
      <node TEXT="root" ID="ID_1">
        <node TEXT="child1" ID="ID_2"/>
        <node TEXT="child2" ID="ID_3">
          <node TEXT="grandchild" ID="ID_4"/>
        </node>
      </node>
    </map>
"""
from __future__ import annotations

from pathlib import Path
from lxml import etree

from ..core.base import BaseParser
from ..core.registry import register
from ..core.schemas import Edge, MindMap, Node


@register("parser", "freemind")
class FreeMindParser(BaseParser):
    def parse(self, path: str | Path) -> MindMap:
        path = Path(path)
        tree = etree.parse(str(path))
        root_map = tree.getroot()

        root_node_elem = root_map.find("node")
        if root_node_elem is None:
            raise ValueError(f"В файле {path} нет корневого <node>")

        nodes: list[Node] = []
        edges: list[Edge] = []
        self._counter = 0
        self._walk(root_node_elem, parent_id=None, depth=0,
                   nodes=nodes, edges=edges)

        return MindMap(
            nodes=nodes,
            edges=edges,
            root_id=nodes[0].id,
            source_file=str(path),
            source_format="freemind",
        )

    def _walk(self, elem, parent_id: str | None, depth: int,
              nodes: list[Node], edges: list[Edge]) -> None:
        # Используем ID из файла, иначе генерируем
        nid = elem.get("ID") or f"n{self._counter}"
        self._counter += 1
        text = (elem.get("TEXT") or "").strip()

        # Метаданные: цвет, иконки, прочие атрибуты — складываем целиком
        meta = {k: v for k, v in elem.attrib.items() if k not in ("ID", "TEXT")}

        nodes.append(Node(id=nid, text=text, depth=depth, metadata=meta))

        if parent_id is not None:
            edges.append(Edge(source=parent_id, target=nid))

        for child in elem.findall("node"):
            self._walk(child, parent_id=nid, depth=depth + 1,
                       nodes=nodes, edges=edges)
