<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Пищеварительная система" ID="ID_0">
    <node TEXT="Ротовая полость" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Зубы" ID="ID_2" GOLD_RELATION="has_part">
        <node TEXT="Резцы" ID="ID_3" GOLD_RELATION="has_example"/>
        <node TEXT="Клыки" ID="ID_4" GOLD_RELATION="has_example"/>
        <node TEXT="Коренные зубы" ID="ID_5" GOLD_RELATION="has_example"/>
        <node TEXT="Измельчение пищи" ID="ID_6" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Язык" ID="ID_7" GOLD_RELATION="has_part"/>
      <node TEXT="Слюнные железы" ID="ID_8" GOLD_RELATION="has_part">
        <node TEXT="Слюна" ID="ID_9" GOLD_RELATION="has_part">
          <node TEXT="Амилаза" ID="ID_10" GOLD_RELATION="has_part"/>
        </node>
      </node>
    </node>
    <node TEXT="Глотка" ID="ID_11" GOLD_RELATION="has_part"/>
    <node TEXT="Пищевод" ID="ID_12" GOLD_RELATION="has_part"/>
    <node TEXT="Желудок" ID="ID_13" GOLD_RELATION="has_part">
      <node TEXT="Желудочный сок" ID="ID_14" GOLD_RELATION="has_part">
        <node TEXT="Соляная кислота" ID="ID_15" GOLD_RELATION="has_part"/>
        <node TEXT="Пепсин" ID="ID_16" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Переваривание белков" ID="ID_17" GOLD_RELATION="has_function"/>
      <node TEXT="Кислая среда" ID="ID_18" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Тонкий кишечник" ID="ID_19" GOLD_RELATION="has_part">
      <node TEXT="Двенадцатиперстная кишка" ID="ID_20" GOLD_RELATION="has_part"/>
      <node TEXT="Ворсинки" ID="ID_21" GOLD_RELATION="has_part">
        <node TEXT="Всасывание питательных веществ" ID="ID_22" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Толстый кишечник" ID="ID_23" GOLD_RELATION="has_part">
      <node TEXT="Всасывание воды" ID="ID_24" GOLD_RELATION="has_function"/>
      <node TEXT="Микрофлора" ID="ID_25" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Пищеварительные железы" ID="ID_26" GOLD_RELATION="associated_with">
      <node TEXT="Печень" ID="ID_27" GOLD_RELATION="has_example">
        <node TEXT="Желчь" ID="ID_28" GOLD_RELATION="has_part">
          <node TEXT="Эмульгирование жиров" ID="ID_29" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Обезвреживание ядов" ID="ID_30" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Поджелудочная железа" ID="ID_31" GOLD_RELATION="has_example">
        <node TEXT="Панкреатический сок" ID="ID_32" GOLD_RELATION="has_part"/>
        <node TEXT="Инсулин" ID="ID_33" GOLD_RELATION="has_part"/>
      </node>
    </node>
    <node TEXT="Этапы пищеварения" ID="ID_34" GOLD_RELATION="associated_with">
      <node TEXT="Механическая обработка" ID="ID_35" GOLD_RELATION="has_part">
        <node TEXT="Химическое расщепление" ID="ID_36" GOLD_RELATION="precedes">
          <node TEXT="Всасывание" ID="ID_37" GOLD_RELATION="precedes">
            <node TEXT="Выведение остатков" ID="ID_38" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
    </node>
  </node>
</map>
