<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Митоз" ID="ID_0">
    <node TEXT="Профаза" ID="ID_1" GOLD_RELATION="has_part">
      <node TEXT="Метафаза" ID="ID_2" GOLD_RELATION="precedes">
        <node TEXT="Анафаза" ID="ID_3" GOLD_RELATION="precedes">
          <node TEXT="Телофаза" ID="ID_4" GOLD_RELATION="precedes">
            <node TEXT="Цитокинез" ID="ID_5" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Профаза — события" ID="ID_6" GOLD_RELATION="associated_with">
      <node TEXT="Конденсация хромосом" ID="ID_7" GOLD_RELATION="has_part"/>
      <node TEXT="Распад ядерной оболочки" ID="ID_8" GOLD_RELATION="has_part"/>
      <node TEXT="Образование веретена деления" ID="ID_9" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Метафаза — события" ID="ID_10" GOLD_RELATION="associated_with">
      <node TEXT="Выстраивание хромосом по экватору" ID="ID_11" GOLD_RELATION="has_part"/>
      <node TEXT="Метафазная пластинка" ID="ID_12" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Анафаза — события" ID="ID_13" GOLD_RELATION="associated_with">
      <node TEXT="Расхождение хроматид к полюсам" ID="ID_14" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Телофаза — события" ID="ID_15" GOLD_RELATION="associated_with">
      <node TEXT="Деспирализация хромосом" ID="ID_16" GOLD_RELATION="has_part"/>
      <node TEXT="Формирование ядерных оболочек" ID="ID_17" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Значение" ID="ID_18" GOLD_RELATION="associated_with">
      <node TEXT="Сохранение числа хромосом" ID="ID_19" GOLD_RELATION="has_function"/>
      <node TEXT="Рост организма" ID="ID_20" GOLD_RELATION="has_function"/>
      <node TEXT="Регенерация тканей" ID="ID_21" GOLD_RELATION="has_function"/>
      <node TEXT="Бесполое размножение" ID="ID_22" GOLD_RELATION="has_function"/>
    </node>
  </node>
</map>
