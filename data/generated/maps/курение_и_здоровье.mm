<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Курение" ID="ID_26">
    <node TEXT="Никотин" ID="ID_27" GOLD_RELATION="has_part">
      <node TEXT="Сужение сосудов" ID="ID_28" GOLD_RELATION="causes">
        <node TEXT="Повышение давления" ID="ID_29" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Зависимость" ID="ID_30" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Смолы" ID="ID_31" GOLD_RELATION="has_part">
      <node TEXT="Рак легких" ID="ID_32" GOLD_RELATION="causes"/>
      <node TEXT="Рак гортани" ID="ID_33" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Угарный газ" ID="ID_34" GOLD_RELATION="has_part">
      <node TEXT="Связывание гемоглобина" ID="ID_35" GOLD_RELATION="causes">
        <node TEXT="Кислородное голодание" ID="ID_36" GOLD_RELATION="causes"/>
      </node>
    </node>
    <node TEXT="Последствия" ID="ID_37" GOLD_RELATION="associated_with">
      <node TEXT="Хронический бронхит" ID="ID_38" GOLD_RELATION="causes"/>
      <node TEXT="Инфаркт" ID="ID_39" GOLD_RELATION="causes"/>
      <node TEXT="Преждевременное старение кожи" ID="ID_40" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Пассивное курение" ID="ID_41" GOLD_RELATION="associated_with">
      <node TEXT="Болезни у детей" ID="ID_42" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
