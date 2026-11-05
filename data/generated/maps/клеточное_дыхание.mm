<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Клеточное дыхание" ID="ID_28">
    <node TEXT="Этапы" ID="ID_29" GOLD_RELATION="associated_with">
      <node TEXT="Подготовительный этап" ID="ID_30" GOLD_RELATION="has_part">
        <node TEXT="Гликолиз" ID="ID_31" GOLD_RELATION="precedes">
          <node TEXT="Кислородный этап" ID="ID_32" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
    <node TEXT="Подготовительный этап" ID="ID_33" GOLD_RELATION="has_example">
      <node TEXT="Расщепление полимеров до мономеров" ID="ID_34" GOLD_RELATION="has_part"/>
      <node TEXT="Пищеварительный тракт" ID="ID_35" GOLD_RELATION="associated_with"/>
      <node TEXT="Выделение тепла" ID="ID_36" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Гликолиз" ID="ID_37" GOLD_RELATION="has_example">
      <node TEXT="Бескислородное расщепление глюкозы" ID="ID_38" GOLD_RELATION="has_part"/>
      <node TEXT="Цитоплазма" ID="ID_39" GOLD_RELATION="associated_with"/>
      <node TEXT="Образование 2 молекул АТФ" ID="ID_40" GOLD_RELATION="causes"/>
      <node TEXT="Пировиноградная кислота" ID="ID_41" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Кислородный этап" ID="ID_42" GOLD_RELATION="has_example">
      <node TEXT="Цикл Кребса" ID="ID_43" GOLD_RELATION="has_part">
        <node TEXT="Окислительное фосфорилирование" ID="ID_44" GOLD_RELATION="precedes"/>
      </node>
      <node TEXT="Митохондрии" ID="ID_45" GOLD_RELATION="associated_with"/>
      <node TEXT="Образование 36 молекул АТФ" ID="ID_46" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Итог" ID="ID_47" GOLD_RELATION="associated_with">
      <node TEXT="Углекислый газ" ID="ID_48" GOLD_RELATION="causes"/>
      <node TEXT="Вода" ID="ID_49" GOLD_RELATION="causes"/>
      <node TEXT="Энергия АТФ" ID="ID_50" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
