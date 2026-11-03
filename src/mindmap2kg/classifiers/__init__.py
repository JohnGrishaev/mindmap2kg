"""Классификаторы типов связей."""
from . import dummy  # noqa: F401

# Sklearn — опциональная зависимость.
try:
    from . import sklearn_wrapper  # noqa: F401
except ImportError:
    pass
