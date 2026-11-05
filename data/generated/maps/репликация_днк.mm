<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Репликация ДНК" ID="ID_24">
    <node TEXT="Раскручивание спирали" ID="ID_25" GOLD_RELATION="has_part">
      <node TEXT="Разрыв водородных связей" ID="ID_26" GOLD_RELATION="precedes">
        <node TEXT="Синтез праймеров" ID="ID_27" GOLD_RELATION="precedes">
          <node TEXT="Синтез новых цепей" ID="ID_28" GOLD_RELATION="precedes">
            <node TEXT="Удаление праймеров" ID="ID_29" GOLD_RELATION="precedes">
              <node TEXT="Сшивание фрагментов" ID="ID_30" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Ферменты" ID="ID_31" GOLD_RELATION="associated_with">
      <node TEXT="Хеликаза" ID="ID_32" GOLD_RELATION="has_example">
        <node TEXT="Раскручивание двойной спирали" ID="ID_33" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="ДНК-полимераза" ID="ID_34" GOLD_RELATION="has_example">
        <node TEXT="Синтез новой цепи" ID="ID_35" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Праймаза" ID="ID_36" GOLD_RELATION="has_example">
        <node TEXT="Синтез праймера" ID="ID_37" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Лигаза" ID="ID_38" GOLD_RELATION="has_example">
        <node TEXT="Сшивание фрагментов Оказаки" ID="ID_39" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Свойства" ID="ID_40" GOLD_RELATION="associated_with">
      <node TEXT="Полуконсервативность" ID="ID_41" GOLD_RELATION="has_property"/>
      <node TEXT="Матричный характер" ID="ID_42" GOLD_RELATION="has_property"/>
      <node TEXT="Высокая точность" ID="ID_43" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Цепи" ID="ID_44" GOLD_RELATION="associated_with">
      <node TEXT="Лидирующая цепь" ID="ID_45" GOLD_RELATION="has_example"/>
      <node TEXT="Отстающая цепь" ID="ID_46" GOLD_RELATION="has_example">
        <node TEXT="Фрагменты Оказаки" ID="ID_47" GOLD_RELATION="has_part"/>
      </node>
    </node>
  </node>
</map>
