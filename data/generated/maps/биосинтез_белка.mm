<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Биосинтез белка" ID="ID_67">
    <node TEXT="Транскрипция" ID="ID_68" GOLD_RELATION="has_part">
      <node TEXT="Трансляция" ID="ID_69" GOLD_RELATION="precedes">
        <node TEXT="Посттрансляционная модификация" ID="ID_70" GOLD_RELATION="precedes"/>
      </node>
    </node>
    <node TEXT="Транскрипция — подробно" ID="ID_71" GOLD_RELATION="associated_with">
      <node TEXT="Связывание РНК-полимеразы с промотором" ID="ID_72" GOLD_RELATION="has_part">
        <node TEXT="Элонгация" ID="ID_73" GOLD_RELATION="precedes">
          <node TEXT="Терминация" ID="ID_74" GOLD_RELATION="precedes"/>
        </node>
      </node>
      <node TEXT="Ядро" ID="ID_75" GOLD_RELATION="associated_with"/>
      <node TEXT="Образование иРНК" ID="ID_76" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Трансляция — подробно" ID="ID_77" GOLD_RELATION="associated_with">
      <node TEXT="Инициация" ID="ID_78" GOLD_RELATION="has_part">
        <node TEXT="Элонгация" ID="ID_79" GOLD_RELATION="precedes">
          <node TEXT="Терминация" ID="ID_80" GOLD_RELATION="precedes"/>
        </node>
      </node>
      <node TEXT="Рибосома" ID="ID_81" GOLD_RELATION="associated_with"/>
      <node TEXT="Образование полипептида" ID="ID_82" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Генетический код" ID="ID_83" GOLD_RELATION="associated_with">
      <node TEXT="Триплетность" ID="ID_84" GOLD_RELATION="has_property"/>
      <node TEXT="Однозначность" ID="ID_85" GOLD_RELATION="has_property"/>
      <node TEXT="Вырожденность" ID="ID_86" GOLD_RELATION="has_property"/>
      <node TEXT="Универсальность" ID="ID_87" GOLD_RELATION="has_property"/>
      <node TEXT="Неперекрываемость" ID="ID_88" GOLD_RELATION="has_property"/>
    </node>
  </node>
</map>
