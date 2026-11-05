<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Клеточный цикл" ID="ID_23">
    <node TEXT="Интерфаза" ID="ID_24" GOLD_RELATION="has_part">
      <node TEXT="G1-период" ID="ID_25" GOLD_RELATION="has_part">
        <node TEXT="S-период" ID="ID_26" GOLD_RELATION="precedes">
          <node TEXT="G2-период" ID="ID_27" GOLD_RELATION="precedes"/>
        </node>
      </node>
      <node TEXT="Рост клетки" ID="ID_28" GOLD_RELATION="has_part"/>
      <node TEXT="Репликация ДНК" ID="ID_29" GOLD_RELATION="has_part"/>
      <node TEXT="Синтез белков" ID="ID_30" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Митотическая фаза" ID="ID_31" GOLD_RELATION="has_part">
      <node TEXT="Митоз" ID="ID_32" GOLD_RELATION="has_part"/>
      <node TEXT="Цитокинез" ID="ID_33" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="G0-период" ID="ID_34" GOLD_RELATION="has_part">
      <node TEXT="Покой клетки" ID="ID_35" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Регуляция" ID="ID_36" GOLD_RELATION="associated_with">
      <node TEXT="Циклины" ID="ID_37" GOLD_RELATION="has_part"/>
      <node TEXT="Циклинзависимые киназы" ID="ID_38" GOLD_RELATION="has_part"/>
      <node TEXT="Контрольные точки" ID="ID_39" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Нарушения" ID="ID_40" GOLD_RELATION="associated_with">
      <node TEXT="Неконтролируемое деление" ID="ID_41" GOLD_RELATION="causes">
        <node TEXT="Опухоль" ID="ID_42" GOLD_RELATION="causes"/>
      </node>
    </node>
  </node>
</map>
