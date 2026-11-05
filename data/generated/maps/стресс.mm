<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Стресс" ID="ID_218">
    <node TEXT="Стрессоры" ID="ID_219" GOLD_RELATION="associated_with">
      <node TEXT="Холод" ID="ID_220" GOLD_RELATION="has_example"/>
      <node TEXT="Боль" ID="ID_221" GOLD_RELATION="has_example"/>
      <node TEXT="Конфликт" ID="ID_222" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Стадии" ID="ID_223" GOLD_RELATION="associated_with">
      <node TEXT="Стадия тревоги" ID="ID_224" GOLD_RELATION="has_part">
        <node TEXT="Стадия сопротивления" ID="ID_225" GOLD_RELATION="precedes">
          <node TEXT="Стадия истощения" ID="ID_226" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
    <node TEXT="Выброс адреналина" ID="ID_227" GOLD_RELATION="causes">
      <node TEXT="Учащение пульса" ID="ID_228" GOLD_RELATION="causes"/>
      <node TEXT="Расширение зрачков" ID="ID_229" GOLD_RELATION="causes"/>
      <node TEXT="Повышение давления" ID="ID_230" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Длительный стресс" ID="ID_231" GOLD_RELATION="associated_with">
      <node TEXT="Снижение иммунитета" ID="ID_232" GOLD_RELATION="causes"/>
      <node TEXT="Язва желудка" ID="ID_233" GOLD_RELATION="causes"/>
      <node TEXT="Бессонница" ID="ID_234" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
