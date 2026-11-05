<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Фотосинтез" ID="ID_0">
    <node TEXT="Световая фаза" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Поглощение света хлорофиллом" ID="ID_2" GOLD_RELATION="has_part">
        <node TEXT="Возбуждение электронов" ID="ID_3" GOLD_RELATION="precedes">
          <node TEXT="Фотолиз воды" ID="ID_4" GOLD_RELATION="precedes">
            <node TEXT="Синтез АТФ" ID="ID_5" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
      <node TEXT="Тилакоиды" ID="ID_6" GOLD_RELATION="associated_with"/>
      <node TEXT="Выделение кислорода" ID="ID_7" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Темновая фаза" ID="ID_8" GOLD_RELATION="has_part">
      <node TEXT="Цикл Кальвина" ID="ID_9" GOLD_RELATION="has_part">
        <node TEXT="Фиксация углекислого газа" ID="ID_10" GOLD_RELATION="has_part">
          <node TEXT="Восстановление" ID="ID_11" GOLD_RELATION="precedes">
            <node TEXT="Регенерация рибулозобисфосфата" ID="ID_12" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
      <node TEXT="Строма хлоропласта" ID="ID_13" GOLD_RELATION="associated_with"/>
      <node TEXT="Образование глюкозы" ID="ID_14" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Условия" ID="ID_15" GOLD_RELATION="associated_with">
      <node TEXT="Свет" ID="ID_16" GOLD_RELATION="associated_with"/>
      <node TEXT="Углекислый газ" ID="ID_17" GOLD_RELATION="associated_with"/>
      <node TEXT="Вода" ID="ID_18" GOLD_RELATION="associated_with"/>
      <node TEXT="Хлорофилл" ID="ID_19" GOLD_RELATION="associated_with"/>
    </node>
    <node TEXT="Значение" ID="ID_20" GOLD_RELATION="associated_with">
      <node TEXT="Образование органических веществ" ID="ID_21" GOLD_RELATION="has_function"/>
      <node TEXT="Насыщение атмосферы кислородом" ID="ID_22" GOLD_RELATION="has_function"/>
      <node TEXT="Образование озонового слоя" ID="ID_23" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Типы" ID="ID_24" GOLD_RELATION="associated_with">
      <node TEXT="C3-фотосинтез" ID="ID_25" GOLD_RELATION="has_example"/>
      <node TEXT="C4-фотосинтез" ID="ID_26" GOLD_RELATION="has_example"/>
      <node TEXT="САМ-фотосинтез" ID="ID_27" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
