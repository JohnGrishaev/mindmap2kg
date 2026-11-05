<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Белки" ID="ID_90">
    <node TEXT="Мономеры" ID="ID_91" GOLD_RELATION="associated_with">
      <node TEXT="Аминокислоты" ID="ID_92" GOLD_RELATION="has_part">
        <node TEXT="Заменимые" ID="ID_93" GOLD_RELATION="has_example"/>
        <node TEXT="Незаменимые" ID="ID_94" GOLD_RELATION="has_example">
          <node TEXT="Триптофан" ID="ID_95" GOLD_RELATION="has_example"/>
          <node TEXT="Лизин" ID="ID_96" GOLD_RELATION="has_example"/>
        </node>
      </node>
    </node>
    <node TEXT="Структура" ID="ID_97" GOLD_RELATION="associated_with">
      <node TEXT="Первичная" ID="ID_98" GOLD_RELATION="has_example">
        <node TEXT="Последовательность аминокислот" ID="ID_99" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Вторичная" ID="ID_100" GOLD_RELATION="has_example">
        <node TEXT="Альфа-спираль" ID="ID_101" GOLD_RELATION="has_example"/>
        <node TEXT="Бета-слой" ID="ID_102" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Третичная" ID="ID_103" GOLD_RELATION="has_example">
        <node TEXT="Глобула" ID="ID_104" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Четвертичная" ID="ID_105" GOLD_RELATION="has_example">
        <node TEXT="Гемоглобин" ID="ID_106" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Функции" ID="ID_107" GOLD_RELATION="associated_with">
      <node TEXT="Каталитическая" ID="ID_108" GOLD_RELATION="has_function">
        <node TEXT="Ферменты" ID="ID_109" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Транспортная" ID="ID_110" GOLD_RELATION="has_function">
        <node TEXT="Гемоглобин" ID="ID_111" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Защитная" ID="ID_112" GOLD_RELATION="has_function">
        <node TEXT="Антитела" ID="ID_113" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Сократительная" ID="ID_114" GOLD_RELATION="has_function">
        <node TEXT="Актин" ID="ID_115" GOLD_RELATION="has_example"/>
        <node TEXT="Миозин" ID="ID_116" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Строительная" ID="ID_117" GOLD_RELATION="has_function">
        <node TEXT="Коллаген" ID="ID_118" GOLD_RELATION="has_example"/>
        <node TEXT="Кератин" ID="ID_119" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Регуляторная" ID="ID_120" GOLD_RELATION="has_function">
        <node TEXT="Инсулин" ID="ID_121" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Энергетическая" ID="ID_122" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Денатурация" ID="ID_123" GOLD_RELATION="associated_with">
      <node TEXT="Нагревание" ID="ID_124" GOLD_RELATION="causes"/>
      <node TEXT="Действие кислот" ID="ID_125" GOLD_RELATION="causes"/>
      <node TEXT="Утрата функции" ID="ID_126" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
