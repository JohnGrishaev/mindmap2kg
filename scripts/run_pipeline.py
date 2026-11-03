"""
CLI для запуска пайплайна: python scripts/run_pipeline.py <input.mm> [--config configs/default.yaml]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Триггерим регистрацию плагинов
import mindmap2kg  # noqa: F401
from mindmap2kg.core.artifacts import ArtifactStore
from mindmap2kg.core.config import load_config, load_taxonomy
from mindmap2kg.core.pipeline import Pipeline


def main():
    ap = argparse.ArgumentParser(description="Прогон пайплайна mindmap2kg")
    ap.add_argument("input", help="Путь к файлу mind-map (.mm)")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--interim-dir", default="data/interim")
    args = ap.parse_args()

    if not Path(args.input).exists():
        print(f"ОШИБКА: файл не найден: {args.input}")
        sys.exit(1)

    config = load_config(args.config)
    taxonomy = load_taxonomy(config.taxonomy)
    store = ArtifactStore(args.interim_dir, config.run_id)

    print(f"\n=== Запуск пайплайна ===")
    print(f"  Конфиг:    {args.config}")
    print(f"  Вход:      {args.input}")
    print(f"  Run ID:    {config.run_id}")
    print(f"  Таксономия: v{taxonomy.get('version')} ({len(taxonomy['relations'])} классов)")
    print()

    pipeline = Pipeline(config, store, taxonomy)
    kg = pipeline.run(args.input)

    print(f"\n=== Готово ===")
    print(f"  Узлов в KG:  {len(kg.nodes)}")
    print(f"  Рёбер в KG:  {len(kg.edges)}")


if __name__ == "__main__":
    main()
