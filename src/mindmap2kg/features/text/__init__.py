"""Текстовые признаки (лексика, эмбеддинги)."""

from . import lexical_simple  # noqa: F401

# SBERT — опциональная зависимость (sentence-transformers).
# Импортируем только если установлена, чтобы не падать без extras [text].
try:
    from . import sbert  # noqa: F401
except ImportError:
    pass
