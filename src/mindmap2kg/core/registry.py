"""
Реестр плагинов. Каждый компонент пайплайна (парсер, фичер, классификатор,
экспортёр) регистрируется по строковому имени, которое указывается в YAML-конфиге.

Добавить новый компонент — это создать класс с базовым интерфейсом и навесить
декоратор @register("kind", "name"). Никаких правок в ядре не требуется.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

# kind → name → class
_REGISTRY: dict[str, dict[str, type]] = {
    "parser":     {},
    "pairing":    {},
    "feature":    {},
    "classifier": {},
    "exporter":   {},
}


def register(kind: str, name: str) -> Callable[[type[T]], type[T]]:
    """Декоратор регистрации. Использование:

        @register("parser", "freemind")
        class FreeMindParser(BaseParser): ...
    """
    if kind not in _REGISTRY:
        raise ValueError(f"Неизвестный тип реестра: {kind!r}. "
                         f"Допустимые: {list(_REGISTRY)}")

    def decorator(cls: type[T]) -> type[T]:
        if name in _REGISTRY[kind]:
            raise ValueError(f"{kind} {name!r} уже зарегистрирован "
                             f"({_REGISTRY[kind][name].__name__})")
        _REGISTRY[kind][name] = cls
        return cls

    return decorator


def get(kind: str, name: str) -> type:
    """Получить класс по имени. Кидает KeyError со списком доступного."""
    if name not in _REGISTRY[kind]:
        available = ", ".join(_REGISTRY[kind]) or "(пусто)"
        raise KeyError(f"{kind} {name!r} не зарегистрирован. "
                       f"Доступные: {available}")
    return _REGISTRY[kind][name]


def list_registered(kind: str | None = None) -> dict[str, list[str]]:
    """Перечислить всё зарегистрированное (для отладки и UI)."""
    if kind is not None:
        return {kind: list(_REGISTRY[kind])}
    return {k: list(v) for k, v in _REGISTRY.items()}
