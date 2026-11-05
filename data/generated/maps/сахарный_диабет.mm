<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Сахарный диабет" ID="ID_199">
    <node TEXT="Типы" ID="ID_200" GOLD_RELATION="associated_with">
      <node TEXT="Диабет 1 типа" ID="ID_201" GOLD_RELATION="has_example">
        <node TEXT="Разрушение бета-клеток" ID="ID_202" GOLD_RELATION="associated_with"/>
        <node TEXT="Нехватка инсулина" ID="ID_203" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Диабет 2 типа" ID="ID_204" GOLD_RELATION="has_example">
        <node TEXT="Невосприимчивость клеток к инсулину" ID="ID_205" GOLD_RELATION="has_property"/>
      </node>
    </node>
    <node TEXT="Симптомы" ID="ID_206" GOLD_RELATION="associated_with">
      <node TEXT="Жажда" ID="ID_207" GOLD_RELATION="has_example"/>
      <node TEXT="Частое мочеиспускание" ID="ID_208" GOLD_RELATION="has_example"/>
      <node TEXT="Быстрая утомляемость" ID="ID_209" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Повышение глюкозы в крови" ID="ID_210" GOLD_RELATION="causes">
      <node TEXT="Поражение сосудов" ID="ID_211" GOLD_RELATION="causes">
        <node TEXT="Нарушение зрения" ID="ID_212" GOLD_RELATION="causes"/>
        <node TEXT="Поражение почек" ID="ID_213" GOLD_RELATION="causes"/>
      </node>
    </node>
    <node TEXT="Лечение" ID="ID_214" GOLD_RELATION="associated_with">
      <node TEXT="Инъекции инсулина" ID="ID_215" GOLD_RELATION="has_example"/>
      <node TEXT="Диета" ID="ID_216" GOLD_RELATION="has_example"/>
      <node TEXT="Физическая активность" ID="ID_217" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
