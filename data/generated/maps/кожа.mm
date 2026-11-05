<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Кожа" ID="ID_57">
    <node TEXT="Эпидермис" ID="ID_58" GOLD_RELATION="has_part">
      <node TEXT="Роговой слой" ID="ID_59" GOLD_RELATION="has_part"/>
      <node TEXT="Меланин" ID="ID_60" GOLD_RELATION="has_part">
        <node TEXT="Защита от ультрафиолета" ID="ID_61" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Дерма" ID="ID_62" GOLD_RELATION="has_part">
      <node TEXT="Потовые железы" ID="ID_63" GOLD_RELATION="has_part">
        <node TEXT="Потоотделение" ID="ID_64" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Сальные железы" ID="ID_65" GOLD_RELATION="has_part"/>
      <node TEXT="Волосяные луковицы" ID="ID_66" GOLD_RELATION="has_part"/>
      <node TEXT="Рецепторы" ID="ID_67" GOLD_RELATION="has_part">
        <node TEXT="Осязание" ID="ID_68" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Подкожная жировая клетчатка" ID="ID_69" GOLD_RELATION="has_part">
      <node TEXT="Теплоизоляция" ID="ID_70" GOLD_RELATION="has_function"/>
      <node TEXT="Запас энергии" ID="ID_71" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Ожог" ID="ID_72" GOLD_RELATION="associated_with"/>
    <node TEXT="Солнечный свет" ID="ID_73" GOLD_RELATION="associated_with">
      <node TEXT="Синтез витамина D" ID="ID_74" GOLD_RELATION="causes"/>
      <node TEXT="Загар" ID="ID_75" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
