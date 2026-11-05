<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Земноводные" ID="ID_146">
    <node TEXT="Представители" ID="ID_147" GOLD_RELATION="associated_with">
      <node TEXT="Лягушка" ID="ID_148" GOLD_RELATION="has_example"/>
      <node TEXT="Жаба" ID="ID_149" GOLD_RELATION="has_example"/>
      <node TEXT="Тритон" ID="ID_150" GOLD_RELATION="has_example"/>
      <node TEXT="Саламандра" ID="ID_151" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Строение" ID="ID_152" GOLD_RELATION="associated_with">
      <node TEXT="Голая слизистая кожа" ID="ID_153" GOLD_RELATION="has_part">
        <node TEXT="Кожное дыхание" ID="ID_154" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Легкие" ID="ID_155" GOLD_RELATION="has_part"/>
      <node TEXT="Трехкамерное сердце" ID="ID_156" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Развитие лягушки" ID="ID_157" GOLD_RELATION="associated_with">
      <node TEXT="Икра" ID="ID_158" GOLD_RELATION="has_part">
        <node TEXT="Головастик" ID="ID_159" GOLD_RELATION="precedes">
          <node TEXT="Головастик с конечностями" ID="ID_160" GOLD_RELATION="precedes">
            <node TEXT="Лягушонок" ID="ID_161" GOLD_RELATION="precedes">
              <node TEXT="Взрослая лягушка" ID="ID_162" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Зависимость от воды" ID="ID_163" GOLD_RELATION="has_property"/>
    <node TEXT="Холоднокровность" ID="ID_164" GOLD_RELATION="has_property"/>
  </node>
</map>
