<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Биосфера" ID="ID_101">
    <node TEXT="Учение Вернадского" ID="ID_102" GOLD_RELATION="associated_with"/>
    <node TEXT="Границы" ID="ID_103" GOLD_RELATION="associated_with">
      <node TEXT="Атмосфера" ID="ID_104" GOLD_RELATION="has_part">
        <node TEXT="Озоновый слой" ID="ID_105" GOLD_RELATION="has_part">
          <node TEXT="Защита от ультрафиолета" ID="ID_106" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Гидросфера" ID="ID_107" GOLD_RELATION="has_part"/>
      <node TEXT="Литосфера" ID="ID_108" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Вещество биосферы" ID="ID_109" GOLD_RELATION="associated_with">
      <node TEXT="Живое вещество" ID="ID_110" GOLD_RELATION="has_example"/>
      <node TEXT="Косное вещество" ID="ID_111" GOLD_RELATION="has_example"/>
      <node TEXT="Биогенное вещество" ID="ID_112" GOLD_RELATION="has_example">
        <node TEXT="Нефть" ID="ID_113" GOLD_RELATION="has_example"/>
        <node TEXT="Каменный уголь" ID="ID_114" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Биокосное вещество" ID="ID_115" GOLD_RELATION="has_example">
        <node TEXT="Почва" ID="ID_116" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Круговорот веществ" ID="ID_117" GOLD_RELATION="associated_with">
      <node TEXT="Круговорот углерода" ID="ID_118" GOLD_RELATION="has_example"/>
      <node TEXT="Круговорот азота" ID="ID_119" GOLD_RELATION="has_example">
        <node TEXT="Азотфиксация" ID="ID_120" GOLD_RELATION="has_part">
          <node TEXT="Нитрификация" ID="ID_121" GOLD_RELATION="precedes">
            <node TEXT="Денитрификация" ID="ID_122" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
      <node TEXT="Круговорот воды" ID="ID_123" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Глобальные проблемы" ID="ID_124" GOLD_RELATION="associated_with">
      <node TEXT="Парниковый эффект" ID="ID_125" GOLD_RELATION="has_example">
        <node TEXT="Сжигание топлива" ID="ID_126" GOLD_RELATION="associated_with"/>
        <node TEXT="Потепление климата" ID="ID_127" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Разрушение озонового слоя" ID="ID_128" GOLD_RELATION="has_example">
        <node TEXT="Фреоны" ID="ID_129" GOLD_RELATION="associated_with"/>
      </node>
      <node TEXT="Опустынивание" ID="ID_130" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
