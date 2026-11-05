<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Нервная система" ID="ID_129">
    <node TEXT="Центральная нервная система" ID="ID_130" GOLD_RELATION="has_part">
      <node TEXT="Головной мозг" ID="ID_131" GOLD_RELATION="has_part">
        <node TEXT="Кора больших полушарий" ID="ID_132" GOLD_RELATION="has_part">
          <node TEXT="Мышление" ID="ID_133" GOLD_RELATION="has_function"/>
          <node TEXT="Речь" ID="ID_134" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Мозжечок" ID="ID_135" GOLD_RELATION="has_part">
          <node TEXT="Координация движений" ID="ID_136" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Продолговатый мозг" ID="ID_137" GOLD_RELATION="has_part">
          <node TEXT="Регуляция дыхания" ID="ID_138" GOLD_RELATION="has_function"/>
        </node>
        <node TEXT="Промежуточный мозг" ID="ID_139" GOLD_RELATION="has_part">
          <node TEXT="Гипоталамус" ID="ID_140" GOLD_RELATION="has_part"/>
        </node>
      </node>
      <node TEXT="Спинной мозг" ID="ID_141" GOLD_RELATION="has_part">
        <node TEXT="Серое вещество" ID="ID_142" GOLD_RELATION="has_part"/>
        <node TEXT="Белое вещество" ID="ID_143" GOLD_RELATION="has_part"/>
        <node TEXT="Рефлекторная функция" ID="ID_144" GOLD_RELATION="has_function"/>
        <node TEXT="Проводниковая функция" ID="ID_145" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Периферическая нервная система" ID="ID_146" GOLD_RELATION="has_part">
      <node TEXT="Нервы" ID="ID_147" GOLD_RELATION="has_part"/>
      <node TEXT="Нервные узлы" ID="ID_148" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Отделы по функциям" ID="ID_149" GOLD_RELATION="associated_with">
      <node TEXT="Соматическая" ID="ID_150" GOLD_RELATION="has_example"/>
      <node TEXT="Вегетативная" ID="ID_151" GOLD_RELATION="has_example">
        <node TEXT="Симпатическая" ID="ID_152" GOLD_RELATION="has_example"/>
        <node TEXT="Парасимпатическая" ID="ID_153" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Нейрон" ID="ID_154" GOLD_RELATION="has_part">
      <node TEXT="Тело нейрона" ID="ID_155" GOLD_RELATION="has_part"/>
      <node TEXT="Дендриты" ID="ID_156" GOLD_RELATION="has_part"/>
      <node TEXT="Аксон" ID="ID_157" GOLD_RELATION="has_part">
        <node TEXT="Миелиновая оболочка" ID="ID_158" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Возбудимость" ID="ID_159" GOLD_RELATION="has_property"/>
      <node TEXT="Проводимость" ID="ID_160" GOLD_RELATION="has_property"/>
    </node>
  </node>
</map>
