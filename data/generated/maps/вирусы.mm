<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Вирусы" ID="ID_165">
    <node TEXT="Строение" ID="ID_166" GOLD_RELATION="associated_with">
      <node TEXT="Нуклеиновая кислота" ID="ID_167" GOLD_RELATION="has_part">
        <node TEXT="ДНК-вирусы" ID="ID_168" GOLD_RELATION="has_example"/>
        <node TEXT="РНК-вирусы" ID="ID_169" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Капсид" ID="ID_170" GOLD_RELATION="has_part">
        <node TEXT="Защита генома" ID="ID_171" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Липидная оболочка" ID="ID_172" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Свойства" ID="ID_173" GOLD_RELATION="associated_with">
      <node TEXT="Неклеточная форма жизни" ID="ID_174" GOLD_RELATION="has_property"/>
      <node TEXT="Облигатный паразитизм" ID="ID_175" GOLD_RELATION="has_property"/>
      <node TEXT="Размножение только в клетке" ID="ID_176" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Жизненный цикл" ID="ID_177" GOLD_RELATION="associated_with">
      <node TEXT="Прикрепление к клетке" ID="ID_178" GOLD_RELATION="has_part">
        <node TEXT="Проникновение" ID="ID_179" GOLD_RELATION="precedes">
          <node TEXT="Синтез вирусных компонентов" ID="ID_180" GOLD_RELATION="precedes">
            <node TEXT="Сборка вирионов" ID="ID_181" GOLD_RELATION="precedes">
              <node TEXT="Выход из клетки" ID="ID_182" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Заболевания" ID="ID_183" GOLD_RELATION="associated_with">
      <node TEXT="Вирус гриппа" ID="ID_184" GOLD_RELATION="has_example">
        <node TEXT="Грипп" ID="ID_185" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="ВИЧ" ID="ID_186" GOLD_RELATION="has_example">
        <node TEXT="СПИД" ID="ID_187" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Коронавирус" ID="ID_188" GOLD_RELATION="has_example">
        <node TEXT="COVID-19" ID="ID_189" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Вирус табачной мозаики" ID="ID_190" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Бактериофаги" ID="ID_191" GOLD_RELATION="has_example">
      <node TEXT="Уничтожение бактерий" ID="ID_192" GOLD_RELATION="has_function"/>
    </node>
  </node>
</map>
