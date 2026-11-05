<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Жизненный цикл папоротника" ID="ID_165">
    <node TEXT="Спорофит" ID="ID_166" GOLD_RELATION="has_part">
      <node TEXT="Спорангии" ID="ID_167" GOLD_RELATION="has_part">
        <node TEXT="Споры" ID="ID_168" GOLD_RELATION="has_part"/>
      </node>
    </node>
    <node TEXT="Стадии" ID="ID_169" GOLD_RELATION="associated_with">
      <node TEXT="Спора" ID="ID_170" GOLD_RELATION="has_part">
        <node TEXT="Заросток" ID="ID_171" GOLD_RELATION="precedes">
          <node TEXT="Гаметы" ID="ID_172" GOLD_RELATION="precedes">
            <node TEXT="Оплодотворение" ID="ID_173" GOLD_RELATION="precedes">
              <node TEXT="Зигота" ID="ID_174" GOLD_RELATION="precedes">
                <node TEXT="Новый спорофит" ID="ID_175" GOLD_RELATION="precedes"/>
              </node>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Зависимость от воды" ID="ID_176" GOLD_RELATION="has_property"/>
    <node TEXT="Чередование поколений" ID="ID_177" GOLD_RELATION="has_property"/>
  </node>
</map>
