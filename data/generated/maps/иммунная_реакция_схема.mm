<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Попадание бактерии в рану" ID="ID_131">
    <node TEXT="Воспаление" ID="ID_132" GOLD_RELATION="causes">
      <node TEXT="Покраснение" ID="ID_133" GOLD_RELATION="causes"/>
      <node TEXT="Отек" ID="ID_134" GOLD_RELATION="causes"/>
      <node TEXT="Повышение температуры" ID="ID_135" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Выход лейкоцитов" ID="ID_136" GOLD_RELATION="causes">
      <node TEXT="Фагоцитоз" ID="ID_137" GOLD_RELATION="precedes">
        <node TEXT="Образование гноя" ID="ID_138" GOLD_RELATION="precedes">
          <node TEXT="Заживление" ID="ID_139" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
  </node>
</map>
