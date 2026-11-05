<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Дыхательная система" ID="ID_99">
    <node TEXT="Воздухоносные пути" ID="ID_100" GOLD_RELATION="has_part">
      <node TEXT="Носовая полость" ID="ID_101" GOLD_RELATION="has_part">
        <node TEXT="Согревание воздуха" ID="ID_102" GOLD_RELATION="has_function"/>
        <node TEXT="Очищение воздуха" ID="ID_103" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Гортань" ID="ID_104" GOLD_RELATION="has_part">
        <node TEXT="Голосовые связки" ID="ID_105" GOLD_RELATION="has_part">
          <node TEXT="Образование звука" ID="ID_106" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Трахея" ID="ID_107" GOLD_RELATION="has_part">
        <node TEXT="Хрящевые полукольца" ID="ID_108" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Бронхи" ID="ID_109" GOLD_RELATION="has_part">
        <node TEXT="Бронхиолы" ID="ID_110" GOLD_RELATION="has_part"/>
      </node>
    </node>
    <node TEXT="Легкие" ID="ID_111" GOLD_RELATION="has_part">
      <node TEXT="Альвеолы" ID="ID_112" GOLD_RELATION="has_part">
        <node TEXT="Газообмен" ID="ID_113" GOLD_RELATION="has_function"/>
        <node TEXT="Тонкая стенка" ID="ID_114" GOLD_RELATION="has_property"/>
      </node>
      <node TEXT="Плевра" ID="ID_115" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Механизм дыхания" ID="ID_116" GOLD_RELATION="associated_with">
      <node TEXT="Вдох" ID="ID_117" GOLD_RELATION="has_part">
        <node TEXT="Выдох" ID="ID_118" GOLD_RELATION="precedes"/>
      </node>
      <node TEXT="Диафрагма" ID="ID_119" GOLD_RELATION="associated_with"/>
      <node TEXT="Межреберные мышцы" ID="ID_120" GOLD_RELATION="associated_with"/>
    </node>
    <node TEXT="Заболевания" ID="ID_121" GOLD_RELATION="associated_with">
      <node TEXT="Бронхит" ID="ID_122" GOLD_RELATION="has_example"/>
      <node TEXT="Пневмония" ID="ID_123" GOLD_RELATION="has_example"/>
      <node TEXT="Туберкулез" ID="ID_124" GOLD_RELATION="has_example">
        <node TEXT="Палочка Коха" ID="ID_125" GOLD_RELATION="associated_with"/>
      </node>
    </node>
    <node TEXT="Курение" ID="ID_126" GOLD_RELATION="associated_with">
      <node TEXT="Рак легких" ID="ID_127" GOLD_RELATION="causes"/>
      <node TEXT="Хронический бронхит" ID="ID_128" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
