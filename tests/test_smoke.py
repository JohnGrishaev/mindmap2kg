"""Smoke-тест: проверяем, что все плагины зарегистрированы."""
import mindmap2kg  # noqa: F401
from mindmap2kg.core.registry import list_registered


def test_all_plugins_registered():
    reg = list_registered()
    assert "freemind" in reg["parser"]
    assert "parent_child" in reg["pairing"]
    assert "lexical_simple" in reg["feature"]
    assert "topology" in reg["feature"]
    assert "dummy" in reg["classifier"]
    assert "graphml" in reg["exporter"]
    assert "jsonld" in reg["exporter"]


def test_registry_listing():
    reg = list_registered()
    for kind in ["parser", "pairing", "feature", "classifier", "exporter"]:
        assert kind in reg
        assert len(reg[kind]) >= 1, f"Нет плагинов типа {kind}"


if __name__ == "__main__":
    test_all_plugins_registered()
    test_registry_listing()
    print("✓ Все smoke-тесты прошли")
    from mindmap2kg.core.registry import list_registered
    for k, v in list_registered().items():
        print(f"  {k}: {v}")
