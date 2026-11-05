<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Кровь" ID="ID_68">
    <node TEXT="Плазма" ID="ID_69" GOLD_RELATION="has_part">
      <node TEXT="Вода" ID="ID_70" GOLD_RELATION="has_part"/>
      <node TEXT="Белки плазмы" ID="ID_71" GOLD_RELATION="has_part">
        <node TEXT="Альбумины" ID="ID_72" GOLD_RELATION="has_example"/>
        <node TEXT="Глобулины" ID="ID_73" GOLD_RELATION="has_example"/>
        <node TEXT="Фибриноген" ID="ID_74" GOLD_RELATION="has_example">
          <node TEXT="Свертывание крови" ID="ID_75" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Минеральные соли" ID="ID_76" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Форменные элементы" ID="ID_77" GOLD_RELATION="has_part">
      <node TEXT="Эритроциты" ID="ID_78" GOLD_RELATION="has_example">
        <node TEXT="Гемоглобин" ID="ID_79" GOLD_RELATION="has_part">
          <node TEXT="Перенос кислорода" ID="ID_80" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Двояковогнутая форма" ID="ID_81" GOLD_RELATION="has_property"/>
        <node TEXT="Отсутствие ядра" ID="ID_82" GOLD_RELATION="has_property"/>
      </node>
      <node TEXT="Лейкоциты" ID="ID_83" GOLD_RELATION="has_example">
        <node TEXT="Нейтрофилы" ID="ID_84" GOLD_RELATION="has_example"/>
        <node TEXT="Лимфоциты" ID="ID_85" GOLD_RELATION="has_example"/>
        <node TEXT="Моноциты" ID="ID_86" GOLD_RELATION="has_example"/>
        <node TEXT="Защита от инфекций" ID="ID_87" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Тромбоциты" ID="ID_88" GOLD_RELATION="has_example">
        <node TEXT="Свертывание крови" ID="ID_89" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Функции крови" ID="ID_90" GOLD_RELATION="associated_with">
      <node TEXT="Транспортная" ID="ID_91" GOLD_RELATION="has_function"/>
      <node TEXT="Защитная" ID="ID_92" GOLD_RELATION="has_function"/>
      <node TEXT="Терморегуляция" ID="ID_93" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Нарушения" ID="ID_94" GOLD_RELATION="associated_with">
      <node TEXT="Анемия" ID="ID_95" GOLD_RELATION="has_example">
        <node TEXT="Недостаток железа" ID="ID_96" GOLD_RELATION="associated_with"/>
        <node TEXT="Слабость" ID="ID_97" GOLD_RELATION="causes"/>
      </node>
      <node TEXT="Гемофилия" ID="ID_98" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
