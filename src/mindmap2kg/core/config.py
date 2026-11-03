"""
Загрузка YAML-конфига пайплайна. Конфиг описывает один эксперимент:
какие компоненты используются и с какими параметрами.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


@dataclass
class ComponentSpec:
    """Спецификация одного компонента: имя в реестре + опции конструктора."""
    name: str
    options: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, x: str | dict) -> ComponentSpec:
        """Принимает либо строку 'name', либо словарь {name, options}."""
        if isinstance(x, str):
            return cls(name=x)
        return cls(name=x["name"], options=x.get("options", {}))


@dataclass
class PipelineConfig:
    run_id: str
    taxonomy: str
    parser: ComponentSpec
    pairing: ComponentSpec
    features: list[ComponentSpec]
    classifier: ComponentSpec
    exporters: list[ComponentSpec]


def load_config(path: str | Path) -> PipelineConfig:
    """Прочитать YAML и валидировать структуру."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    try:
        return PipelineConfig(
            run_id=data["run_id"],
            taxonomy=data["taxonomy"],
            parser=ComponentSpec.from_any(data["parser"]),
            pairing=ComponentSpec.from_any(data["pairing"]),
            features=[ComponentSpec.from_any(f) for f in data["features"]],
            classifier=ComponentSpec.from_any(data["classifier"]),
            exporters=[ComponentSpec.from_any(e) for e in data["exporters"]],
        )
    except KeyError as e:
        raise ValueError(f"В конфиге {path} отсутствует обязательное поле: {e}") from e


def load_taxonomy(path: str | Path) -> dict:
    """Загрузить taxonomy.yaml как dict (без строгой валидации, пока)."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
