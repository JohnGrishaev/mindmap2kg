<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Экосистема" ID="ID_0">
    <node TEXT="Биотические компоненты" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Продуценты" ID="ID_2" GOLD_RELATION="has_example">
        <node TEXT="Зеленые растения" ID="ID_3" GOLD_RELATION="has_example"/>
        <node TEXT="Цианобактерии" ID="ID_4" GOLD_RELATION="has_example"/>
        <node TEXT="Создание органических веществ" ID="ID_5" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Консументы" ID="ID_6" GOLD_RELATION="has_example">
        <node TEXT="Консументы первого порядка" ID="ID_7" GOLD_RELATION="has_example">
          <node TEXT="Травоядные животные" ID="ID_8" GOLD_RELATION="has_example"/>
        </node>
        <node TEXT="Консументы второго порядка" ID="ID_9" GOLD_RELATION="has_example">
          <node TEXT="Хищники" ID="ID_10" GOLD_RELATION="has_example"/>
        </node>
        <node TEXT="Потребление органических веществ" ID="ID_11" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Редуценты" ID="ID_12" GOLD_RELATION="has_example">
        <node TEXT="Бактерии гниения" ID="ID_13" GOLD_RELATION="has_example"/>
        <node TEXT="Грибы" ID="ID_14" GOLD_RELATION="has_example"/>
        <node TEXT="Разложение органических остатков" ID="ID_15" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Абиотические компоненты" ID="ID_16" GOLD_RELATION="has_part">
      <node TEXT="Свет" ID="ID_17" GOLD_RELATION="has_example"/>
      <node TEXT="Температура" ID="ID_18" GOLD_RELATION="has_example"/>
      <node TEXT="Влажность" ID="ID_19" GOLD_RELATION="has_example"/>
      <node TEXT="Почва" ID="ID_20" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Свойства" ID="ID_21" GOLD_RELATION="associated_with">
      <node TEXT="Саморегуляция" ID="ID_22" GOLD_RELATION="has_property"/>
      <node TEXT="Устойчивость" ID="ID_23" GOLD_RELATION="has_property"/>
      <node TEXT="Целостность" ID="ID_24" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Примеры" ID="ID_25" GOLD_RELATION="associated_with">
      <node TEXT="Лес" ID="ID_26" GOLD_RELATION="has_example"/>
      <node TEXT="Озеро" ID="ID_27" GOLD_RELATION="has_example"/>
      <node TEXT="Луг" ID="ID_28" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
