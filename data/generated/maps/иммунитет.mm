<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Иммунитет" ID="ID_203">
    <node TEXT="Виды иммунитета" ID="ID_204" GOLD_RELATION="associated_with">
      <node TEXT="Врожденный" ID="ID_205" GOLD_RELATION="has_example"/>
      <node TEXT="Приобретенный" ID="ID_206" GOLD_RELATION="has_example">
        <node TEXT="Естественный" ID="ID_207" GOLD_RELATION="has_example">
          <node TEXT="После болезни" ID="ID_208" GOLD_RELATION="has_example"/>
        </node>
        <node TEXT="Искусственный" ID="ID_209" GOLD_RELATION="has_example">
          <node TEXT="Активный" ID="ID_210" GOLD_RELATION="has_example">
            <node TEXT="Вакцина" ID="ID_211" GOLD_RELATION="associated_with"/>
          </node>
          <node TEXT="Пассивный" ID="ID_212" GOLD_RELATION="has_example">
            <node TEXT="Лечебная сыворотка" ID="ID_213" GOLD_RELATION="associated_with"/>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Органы иммунной системы" ID="ID_214" GOLD_RELATION="associated_with">
      <node TEXT="Красный костный мозг" ID="ID_215" GOLD_RELATION="has_example"/>
      <node TEXT="Тимус" ID="ID_216" GOLD_RELATION="has_example"/>
      <node TEXT="Лимфатические узлы" ID="ID_217" GOLD_RELATION="has_example"/>
      <node TEXT="Селезенка" ID="ID_218" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Клетки" ID="ID_219" GOLD_RELATION="associated_with">
      <node TEXT="Фагоциты" ID="ID_220" GOLD_RELATION="has_example">
        <node TEXT="Фагоцитоз" ID="ID_221" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="T-лимфоциты" ID="ID_222" GOLD_RELATION="has_example">
        <node TEXT="Уничтожение зараженных клеток" ID="ID_223" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="B-лимфоциты" ID="ID_224" GOLD_RELATION="has_example">
        <node TEXT="Синтез антител" ID="ID_225" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Иммунный ответ" ID="ID_226" GOLD_RELATION="associated_with">
      <node TEXT="Распознавание антигена" ID="ID_227" GOLD_RELATION="has_part">
        <node TEXT="Активация лимфоцитов" ID="ID_228" GOLD_RELATION="precedes">
          <node TEXT="Выработка антител" ID="ID_229" GOLD_RELATION="precedes">
            <node TEXT="Уничтожение антигена" ID="ID_230" GOLD_RELATION="precedes">
              <node TEXT="Формирование клеток памяти" ID="ID_231" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="ВИЧ" ID="ID_232" GOLD_RELATION="associated_with">
      <node TEXT="Разрушение T-лимфоцитов" ID="ID_233" GOLD_RELATION="causes">
        <node TEXT="СПИД" ID="ID_234" GOLD_RELATION="causes"/>
      </node>
    </node>
  </node>
</map>
