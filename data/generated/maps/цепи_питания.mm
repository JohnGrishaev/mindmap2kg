<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Цепи питания" ID="ID_29">
    <node TEXT="Пастбищная цепь" ID="ID_30" GOLD_RELATION="has_example">
      <node TEXT="Растения" ID="ID_31" GOLD_RELATION="has_part">
        <node TEXT="Растительноядные животные" ID="ID_32" GOLD_RELATION="precedes">
          <node TEXT="Хищники первого порядка" ID="ID_33" GOLD_RELATION="precedes">
            <node TEXT="Хищники второго порядка" ID="ID_34" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Детритная цепь" ID="ID_35" GOLD_RELATION="has_example">
      <node TEXT="Опавшие листья" ID="ID_36" GOLD_RELATION="has_part">
        <node TEXT="Дождевые черви" ID="ID_37" GOLD_RELATION="precedes">
          <node TEXT="Кроты" ID="ID_38" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
    <node TEXT="Пример цепи" ID="ID_39" GOLD_RELATION="associated_with">
      <node TEXT="Трава" ID="ID_40" GOLD_RELATION="has_part">
        <node TEXT="Кузнечик" ID="ID_41" GOLD_RELATION="precedes">
          <node TEXT="Лягушка" ID="ID_42" GOLD_RELATION="precedes">
            <node TEXT="Уж" ID="ID_43" GOLD_RELATION="precedes">
              <node TEXT="Орел" ID="ID_44" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Правило экологической пирамиды" ID="ID_45" GOLD_RELATION="associated_with">
      <node TEXT="Передача 10 процентов энергии" ID="ID_46" GOLD_RELATION="has_property"/>
      <node TEXT="Сокращение биомассы на каждом уровне" ID="ID_47" GOLD_RELATION="has_property"/>
    </node>
  </node>
</map>
