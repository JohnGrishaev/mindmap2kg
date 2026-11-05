<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Нервный импульс" ID="ID_150">
    <node TEXT="Потенциал покоя" ID="ID_151" GOLD_RELATION="has_part">
      <node TEXT="Деполяризация" ID="ID_152" GOLD_RELATION="precedes">
        <node TEXT="Потенциал действия" ID="ID_153" GOLD_RELATION="precedes">
          <node TEXT="Реполяризация" ID="ID_154" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
    <node TEXT="Синапс" ID="ID_155" GOLD_RELATION="associated_with">
      <node TEXT="Пресинаптическая мембрана" ID="ID_156" GOLD_RELATION="has_part"/>
      <node TEXT="Синаптическая щель" ID="ID_157" GOLD_RELATION="has_part"/>
      <node TEXT="Постсинаптическая мембрана" ID="ID_158" GOLD_RELATION="has_part"/>
      <node TEXT="Медиатор" ID="ID_159" GOLD_RELATION="has_part">
        <node TEXT="Ацетилхолин" ID="ID_160" GOLD_RELATION="has_example"/>
        <node TEXT="Дофамин" ID="ID_161" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Скорость проведения" ID="ID_162" GOLD_RELATION="has_property"/>
    <node TEXT="Миелин" ID="ID_163" GOLD_RELATION="associated_with">
      <node TEXT="Ускорение проведения" ID="ID_164" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
