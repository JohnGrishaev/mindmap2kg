<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Семя" ID="ID_114">
    <node TEXT="Строение" ID="ID_115" GOLD_RELATION="associated_with">
      <node TEXT="Семенная кожура" ID="ID_116" GOLD_RELATION="has_part">
        <node TEXT="Защита зародыша" ID="ID_117" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Зародыш" ID="ID_118" GOLD_RELATION="has_part">
        <node TEXT="Корешок" ID="ID_119" GOLD_RELATION="has_part"/>
        <node TEXT="Стебелек" ID="ID_120" GOLD_RELATION="has_part"/>
        <node TEXT="Почечка" ID="ID_121" GOLD_RELATION="has_part"/>
        <node TEXT="Семядоли" ID="ID_122" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Эндосперм" ID="ID_123" GOLD_RELATION="has_part">
        <node TEXT="Запас питательных веществ" ID="ID_124" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Условия прорастания" ID="ID_125" GOLD_RELATION="associated_with">
      <node TEXT="Вода" ID="ID_126" GOLD_RELATION="associated_with"/>
      <node TEXT="Воздух" ID="ID_127" GOLD_RELATION="associated_with"/>
      <node TEXT="Тепло" ID="ID_128" GOLD_RELATION="associated_with"/>
    </node>
    <node TEXT="Прорастание" ID="ID_129" GOLD_RELATION="associated_with">
      <node TEXT="Набухание" ID="ID_130" GOLD_RELATION="has_part">
        <node TEXT="Появление корешка" ID="ID_131" GOLD_RELATION="precedes">
          <node TEXT="Появление проростка" ID="ID_132" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
    <node TEXT="Типы семян" ID="ID_133" GOLD_RELATION="associated_with">
      <node TEXT="Однодольные" ID="ID_134" GOLD_RELATION="has_example">
        <node TEXT="Зерновка пшеницы" ID="ID_135" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Двудольные" ID="ID_136" GOLD_RELATION="has_example">
        <node TEXT="Семя фасоли" ID="ID_137" GOLD_RELATION="has_example"/>
      </node>
    </node>
  </node>
</map>
