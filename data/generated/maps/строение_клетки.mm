<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Клетка" ID="ID_0">
    <node TEXT="Мембрана" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Фосфолипидный бислой" ID="ID_2" GOLD_RELATION="has_part"/>
      <node TEXT="Мембранные белки" ID="ID_3" GOLD_RELATION="has_part">
        <node TEXT="Белки-переносчики" ID="ID_4" GOLD_RELATION="has_example"/>
        <node TEXT="Рецепторы" ID="ID_5" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Избирательная проницаемость" ID="ID_6" GOLD_RELATION="has_property"/>
      <node TEXT="Защита содержимого клетки" ID="ID_7" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Цитоплазма" ID="ID_8" GOLD_RELATION="has_part">
      <node TEXT="Гиалоплазма" ID="ID_9" GOLD_RELATION="has_part"/>
      <node TEXT="Органоиды" ID="ID_10" GOLD_RELATION="has_part"/>
      <node TEXT="Включения" ID="ID_11" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Ядро" ID="ID_12" GOLD_RELATION="has_part">
      <node TEXT="Ядерная оболочка" ID="ID_13" GOLD_RELATION="has_part">
        <node TEXT="Ядерные поры" ID="ID_14" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Ядрышко" ID="ID_15" GOLD_RELATION="has_part">
        <node TEXT="Сборка рибосом" ID="ID_16" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Хроматин" ID="ID_17" GOLD_RELATION="has_part"/>
      <node TEXT="Хранение наследственной информации" ID="ID_18" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Виды клеток" ID="ID_19" GOLD_RELATION="associated_with">
      <node TEXT="Растительная клетка" ID="ID_20" GOLD_RELATION="has_example"/>
      <node TEXT="Животная клетка" ID="ID_21" GOLD_RELATION="has_example"/>
      <node TEXT="Клетка гриба" ID="ID_22" GOLD_RELATION="has_example"/>
      <node TEXT="Бактериальная клетка" ID="ID_23" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
