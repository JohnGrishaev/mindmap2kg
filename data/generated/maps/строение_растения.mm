<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Цветковое растение" ID="ID_0">
    <node TEXT="Корень" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Корневой чехлик" ID="ID_2" GOLD_RELATION="has_part">
        <node TEXT="Защита верхушки корня" ID="ID_3" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Зона деления" ID="ID_4" GOLD_RELATION="has_part"/>
      <node TEXT="Зона роста" ID="ID_5" GOLD_RELATION="has_part"/>
      <node TEXT="Зона всасывания" ID="ID_6" GOLD_RELATION="has_part">
        <node TEXT="Корневые волоски" ID="ID_7" GOLD_RELATION="has_part">
          <node TEXT="Всасывание воды" ID="ID_8" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Закрепление в почве" ID="ID_9" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Побег" ID="ID_10" GOLD_RELATION="has_part">
      <node TEXT="Стебель" ID="ID_11" GOLD_RELATION="has_part">
        <node TEXT="Кора" ID="ID_12" GOLD_RELATION="has_part"/>
        <node TEXT="Камбий" ID="ID_13" GOLD_RELATION="has_part">
          <node TEXT="Рост в толщину" ID="ID_14" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Древесина" ID="ID_15" GOLD_RELATION="has_part">
          <node TEXT="Проведение воды" ID="ID_16" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Сердцевина" ID="ID_17" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Лист" ID="ID_18" GOLD_RELATION="has_part">
        <node TEXT="Листовая пластинка" ID="ID_19" GOLD_RELATION="has_part"/>
        <node TEXT="Черешок" ID="ID_20" GOLD_RELATION="has_part"/>
        <node TEXT="Устьица" ID="ID_21" GOLD_RELATION="has_part">
          <node TEXT="Газообмен" ID="ID_22" GOLD_RELATION="has_function"/>
          <node TEXT="Испарение воды" ID="ID_23" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Фотосинтез" ID="ID_24" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Почки" ID="ID_25" GOLD_RELATION="has_part">
        <node TEXT="Вегетативные" ID="ID_26" GOLD_RELATION="has_example"/>
        <node TEXT="Генеративные" ID="ID_27" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Цветок" ID="ID_28" GOLD_RELATION="has_part">
      <node TEXT="Чашечка" ID="ID_29" GOLD_RELATION="has_part"/>
      <node TEXT="Венчик" ID="ID_30" GOLD_RELATION="has_part"/>
      <node TEXT="Тычинки" ID="ID_31" GOLD_RELATION="has_part">
        <node TEXT="Пыльник" ID="ID_32" GOLD_RELATION="has_part">
          <node TEXT="Пыльца" ID="ID_33" GOLD_RELATION="has_part"/>
        </node>
      </node>
      <node TEXT="Пестик" ID="ID_34" GOLD_RELATION="has_part">
        <node TEXT="Рыльце" ID="ID_35" GOLD_RELATION="has_part"/>
        <node TEXT="Столбик" ID="ID_36" GOLD_RELATION="has_part"/>
        <node TEXT="Завязь" ID="ID_37" GOLD_RELATION="has_part">
          <node TEXT="Семязачаток" ID="ID_38" GOLD_RELATION="has_part"/>
        </node>
      </node>
      <node TEXT="Размножение" ID="ID_39" GOLD_RELATION="has_function"/>
    </node>
  </node>
</map>
