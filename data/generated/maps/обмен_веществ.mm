<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Обмен веществ" ID="ID_87">
    <node TEXT="Ассимиляция" ID="ID_88" GOLD_RELATION="has_part">
      <node TEXT="Синтез белков" ID="ID_89" GOLD_RELATION="has_example"/>
      <node TEXT="Фотосинтез" ID="ID_90" GOLD_RELATION="has_example"/>
      <node TEXT="Хемосинтез" ID="ID_91" GOLD_RELATION="has_example"/>
      <node TEXT="Затрата энергии" ID="ID_92" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Диссимиляция" ID="ID_93" GOLD_RELATION="has_part">
      <node TEXT="Клеточное дыхание" ID="ID_94" GOLD_RELATION="has_example"/>
      <node TEXT="Брожение" ID="ID_95" GOLD_RELATION="has_example"/>
      <node TEXT="Выделение энергии" ID="ID_96" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Типы питания" ID="ID_97" GOLD_RELATION="associated_with">
      <node TEXT="Автотрофы" ID="ID_98" GOLD_RELATION="has_example">
        <node TEXT="Фототрофы" ID="ID_99" GOLD_RELATION="has_example">
          <node TEXT="Зеленые растения" ID="ID_100" GOLD_RELATION="has_example"/>
        </node>
        <node TEXT="Хемотрофы" ID="ID_101" GOLD_RELATION="has_example">
          <node TEXT="Нитрифицирующие бактерии" ID="ID_102" GOLD_RELATION="has_example"/>
        </node>
      </node>
      <node TEXT="Гетеротрофы" ID="ID_103" GOLD_RELATION="has_example">
        <node TEXT="Животные" ID="ID_104" GOLD_RELATION="has_example"/>
        <node TEXT="Грибы" ID="ID_105" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Миксотрофы" ID="ID_106" GOLD_RELATION="has_example">
        <node TEXT="Эвглена зеленая" ID="ID_107" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Нарушения обмена" ID="ID_108" GOLD_RELATION="associated_with">
      <node TEXT="Ожирение" ID="ID_109" GOLD_RELATION="has_example">
        <node TEXT="Переедание" ID="ID_110" GOLD_RELATION="associated_with"/>
        <node TEXT="Сахарный диабет 2 типа" ID="ID_111" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Подагра" ID="ID_112" GOLD_RELATION="has_example">
        <node TEXT="Отложение солей мочевой кислоты" ID="ID_113" GOLD_RELATION="causes"/>
      </node>
    </node>
  </node>
</map>
