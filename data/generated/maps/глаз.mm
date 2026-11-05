<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Глаз" ID="ID_17">
    <node TEXT="Склера" ID="ID_18" GOLD_RELATION="has_part"/>
    <node TEXT="Роговица" ID="ID_19" GOLD_RELATION="has_part">
      <node TEXT="Прозрачность" ID="ID_20" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Радужка" ID="ID_21" GOLD_RELATION="has_part">
      <node TEXT="Цвет глаз" ID="ID_22" GOLD_RELATION="has_property"/>
      <node TEXT="Зрачок" ID="ID_23" GOLD_RELATION="has_part">
        <node TEXT="Регуляция света" ID="ID_24" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Хрусталик" ID="ID_25" GOLD_RELATION="has_part">
      <node TEXT="Фокусировка" ID="ID_26" GOLD_RELATION="has_function"/>
      <node TEXT="Эластичность" ID="ID_27" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Стекловидное тело" ID="ID_28" GOLD_RELATION="has_part"/>
    <node TEXT="Сетчатка" ID="ID_29" GOLD_RELATION="has_part">
      <node TEXT="Палочки" ID="ID_30" GOLD_RELATION="has_part">
        <node TEXT="Сумеречное зрение" ID="ID_31" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Колбочки" ID="ID_32" GOLD_RELATION="has_part">
        <node TEXT="Цветовое зрение" ID="ID_33" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Слепое пятно" ID="ID_34" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Зрительный нерв" ID="ID_35" GOLD_RELATION="has_part"/>
    <node TEXT="Близорукость" ID="ID_36" GOLD_RELATION="associated_with"/>
    <node TEXT="Дальнозоркость" ID="ID_37" GOLD_RELATION="associated_with"/>
    <node TEXT="Катаракта" ID="ID_38" GOLD_RELATION="associated_with"/>
  </node>
</map>
