<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Свертывание крови" ID="ID_140">
    <node TEXT="Повреждение сосуда" ID="ID_141" GOLD_RELATION="has_part">
      <node TEXT="Разрушение тромбоцитов" ID="ID_142" GOLD_RELATION="precedes">
        <node TEXT="Выделение тромбопластина" ID="ID_143" GOLD_RELATION="precedes">
          <node TEXT="Образование тромбина" ID="ID_144" GOLD_RELATION="precedes">
            <node TEXT="Фибриноген в фибрин" ID="ID_145" GOLD_RELATION="precedes">
              <node TEXT="Образование тромба" ID="ID_146" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Кальций" ID="ID_147" GOLD_RELATION="associated_with"/>
    <node TEXT="Витамин K" ID="ID_148" GOLD_RELATION="associated_with"/>
    <node TEXT="Гемофилия" ID="ID_149" GOLD_RELATION="associated_with"/>
  </node>
</map>
