"""
Базовые классы (ABC) для плагинов.

Они задают контракт, который каждый плагин обязан реализовать.
Реальная регистрация — через декоратор @register в самих модулях плагинов.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

from .schemas import CandidatePair, KnowledgeGraph, MindMap, Prediction


class BaseParser(ABC):
    """Парсер: путь к файлу → MindMap."""
    @abstractmethod
    def parse(self, path: str | Path) -> MindMap: ...


class BasePairing(ABC):
    """Стратегия выделения пар-кандидатов из MindMap."""
    @abstractmethod
    def extract(self, mm: MindMap) -> list[CandidatePair]: ...


class BaseFeature(ABC):
    """Извлекатель признаков: расширяет DataFrame новыми колонками.

    Получает MindMap (для графовых признаков) и текущий DataFrame
    (для возможности видеть признаки от предыдущих фичеров).
    """
    @abstractmethod
    def transform(self, df: pd.DataFrame, mm: MindMap) -> pd.DataFrame: ...


class BaseClassifier(ABC):
    """Классификатор. На вход — DataFrame с признаками, на выход — Prediction'ы.

    taxonomy передаётся в конструктор, чтобы классификатор знал список классов.
    """
    def __init__(self, taxonomy: dict, **kwargs): ...

    @abstractmethod
    def predict(self, df: pd.DataFrame) -> list[Prediction]: ...


class BaseExporter(ABC):
    """Сериализация KnowledgeGraph в файл."""
    @abstractmethod
    def export(self, kg: KnowledgeGraph, path: str | Path) -> None: ...

    @abstractmethod
    def extension(self) -> str:
        """Расширение файла без точки (graphml, jsonld, ttl)."""
