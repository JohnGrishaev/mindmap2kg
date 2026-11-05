<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Инфекционные заболевания" ID="ID_0">
    <node TEXT="Возбудители" ID="ID_1" GOLD_RELATION="associated_with">
      <node TEXT="Бактерии" ID="ID_2" GOLD_RELATION="has_example">
        <node TEXT="Чума" ID="ID_3" GOLD_RELATION="causes"/>
        <node TEXT="Холера" ID="ID_4" GOLD_RELATION="causes"/>
        <node TEXT="Дифтерия" ID="ID_5" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Вирусы" ID="ID_6" GOLD_RELATION="has_example">
        <node TEXT="Корь" ID="ID_7" GOLD_RELATION="causes"/>
        <node TEXT="Ветряная оспа" ID="ID_8" GOLD_RELATION="causes"/>
        <node TEXT="Бешенство" ID="ID_9" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Простейшие" ID="ID_10" GOLD_RELATION="has_example">
        <node TEXT="Малярийный плазмодий" ID="ID_11" GOLD_RELATION="has_example">
          <node TEXT="Малярия" ID="ID_12" GOLD_RELATION="causes"/>
        </node>
        <node TEXT="Дизентерийная амеба" ID="ID_13" GOLD_RELATION="has_example">
          <node TEXT="Амебная дизентерия" ID="ID_14" GOLD_RELATION="causes"/>
        </node>
      </node>
    </node>
    <node TEXT="Пути передачи" ID="ID_15" GOLD_RELATION="associated_with">
      <node TEXT="Воздушно-капельный" ID="ID_16" GOLD_RELATION="has_example"/>
      <node TEXT="Контактный" ID="ID_17" GOLD_RELATION="has_example"/>
      <node TEXT="Через воду и пищу" ID="ID_18" GOLD_RELATION="has_example"/>
      <node TEXT="Через кровь" ID="ID_19" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Профилактика" ID="ID_20" GOLD_RELATION="associated_with">
      <node TEXT="Вакцинация" ID="ID_21" GOLD_RELATION="has_example">
        <node TEXT="Формирование иммунитета" ID="ID_22" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Мытье рук" ID="ID_23" GOLD_RELATION="has_example"/>
      <node TEXT="Карантин" ID="ID_24" GOLD_RELATION="has_example">
        <node TEXT="Остановка распространения инфекции" ID="ID_25" GOLD_RELATION="has_function"/>
      </node>
    </node>
  </node>
</map>
