<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Опыление" ID="ID_92">
    <node TEXT="Самоопыление" ID="ID_93" GOLD_RELATION="has_example">
      <node TEXT="Горох" ID="ID_94" GOLD_RELATION="has_example"/>
      <node TEXT="Пшеница" ID="ID_95" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Перекрестное опыление" ID="ID_96" GOLD_RELATION="has_example">
      <node TEXT="Насекомыми" ID="ID_97" GOLD_RELATION="has_example">
        <node TEXT="Яркий венчик" ID="ID_98" GOLD_RELATION="has_property"/>
        <node TEXT="Нектар" ID="ID_99" GOLD_RELATION="has_property"/>
        <node TEXT="Аромат" ID="ID_100" GOLD_RELATION="has_property"/>
      </node>
      <node TEXT="Ветром" ID="ID_101" GOLD_RELATION="has_example">
        <node TEXT="Мелкая сухая пыльца" ID="ID_102" GOLD_RELATION="has_property"/>
        <node TEXT="Невзрачные цветки" ID="ID_103" GOLD_RELATION="has_property"/>
        <node TEXT="Береза" ID="ID_104" GOLD_RELATION="has_example"/>
        <node TEXT="Рожь" ID="ID_105" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Искусственное опыление" ID="ID_106" GOLD_RELATION="has_example"/>
    <node TEXT="Двойное оплодотворение" ID="ID_107" GOLD_RELATION="associated_with">
      <node TEXT="Навашин" ID="ID_108" GOLD_RELATION="associated_with"/>
      <node TEXT="Опыление" ID="ID_109" GOLD_RELATION="has_part">
        <node TEXT="Прорастание пыльцевой трубки" ID="ID_110" GOLD_RELATION="precedes">
          <node TEXT="Слияние спермия с яйцеклеткой" ID="ID_111" GOLD_RELATION="precedes">
            <node TEXT="Слияние второго спермия с центральной клеткой" ID="ID_112" GOLD_RELATION="precedes">
              <node TEXT="Образование зародыша и эндосперма" ID="ID_113" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
  </node>
</map>
