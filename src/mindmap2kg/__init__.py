"""mindmap2kg — преобразование mind-map в граф знаний с разметкой типов связей."""

__version__ = "0.1.0"

# Импорт пакетов плагинов триггерит регистрацию через @register декораторы.
# Порядок важен только в том смысле, что один плагин не должен зависеть от другого.
from . import parsers      # noqa: F401
from . import pairing      # noqa: F401
from . import features     # noqa: F401
from . import classifiers  # noqa: F401
from . import exporters    # noqa: F401
