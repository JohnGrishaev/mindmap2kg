<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Сердце" ID="ID_0">
    <node TEXT="Перикард" ID="ID_1" GOLD_RELATION="has_part"/>
    <node TEXT="Миокард" ID="ID_2" GOLD_RELATION="has_part"/>
    <node TEXT="Эндокард" ID="ID_3" GOLD_RELATION="has_part"/>
    <node TEXT="Левое предсердие" ID="ID_4" GOLD_RELATION="has_part"/>
    <node TEXT="Правое предсердие" ID="ID_5" GOLD_RELATION="has_part"/>
    <node TEXT="Левый желудочек" ID="ID_6" GOLD_RELATION="has_part">
      <node TEXT="Самая толстая стенка" ID="ID_7" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Правый желудочек" ID="ID_8" GOLD_RELATION="has_part"/>
    <node TEXT="Митральный клапан" ID="ID_9" GOLD_RELATION="has_part"/>
    <node TEXT="Трикуспидальный клапан" ID="ID_10" GOLD_RELATION="has_part"/>
    <node TEXT="Насос" ID="ID_11" GOLD_RELATION="has_function"/>
    <node TEXT="Автоматия" ID="ID_12" GOLD_RELATION="has_property"/>
    <node TEXT="Синусовый узел" ID="ID_13" GOLD_RELATION="has_part">
      <node TEXT="Ритм сердца" ID="ID_14" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Тахикардия" ID="ID_15" GOLD_RELATION="associated_with"/>
    <node TEXT="Брадикардия" ID="ID_16" GOLD_RELATION="associated_with"/>
  </node>
</map>
