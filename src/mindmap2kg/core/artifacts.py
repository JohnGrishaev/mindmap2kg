"""
Хранилище промежуточных артефактов между этапами пайплайна.

Каждый запуск с уникальным run_id создаёт подкаталог в base_dir.
В нём сохраняются результаты каждого этапа — это даёт:
  * кэширование (не пересчитываем эмбеддинги при смене классификатора)
  * полный аудит для ВКР (можно показать, какие данные были на каждом шаге)
  * отладку любого этапа отдельно (загрузил артефакт — продолжил с него)

Для прототипа используем JSON и CSV. Когда появятся эмбеддинги, будем
дописывать поддержку Parquet (это будет один параметр в save_table).
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

from .schemas import MindMap


class ArtifactStore:
    def __init__(self, base_dir: str | Path, run_id: str):
        self.base = Path(base_dir) / run_id
        self.base.mkdir(parents=True, exist_ok=True)

    # ---------- mind-map (JSON) ----------

    def save_mindmap(self, mm: MindMap, name: str) -> Path:
        path = self.base / f"{name}.json"
        mm.save(path)
        return path

    def load_mindmap(self, name: str) -> MindMap:
        return MindMap.load(self.base / f"{name}.json")

    # ---------- табличные данные (CSV для прототипа) ----------

    def save_table(self, df: pd.DataFrame, name: str) -> Path:
        path = self.base / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8")
        return path

    def load_table(self, name: str) -> pd.DataFrame:
        return pd.read_csv(self.base / f"{name}.csv", encoding="utf-8")

    # ---------- произвольный JSON ----------

    def save_json(self, data: dict, name: str) -> Path:
        path = self.base / f"{name}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def load_json(self, name: str) -> dict:
        return json.loads((self.base / f"{name}.json").read_text(encoding="utf-8"))

    # ---------- путь для произвольных файлов (экспортёры) ----------

    def path(self, filename: str) -> Path:
        return self.base / filename
