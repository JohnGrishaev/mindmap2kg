<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Гликолиз" ID="ID_51">
    <node TEXT="Глюкоза" ID="ID_52" GOLD_RELATION="associated_with">
      <node TEXT="Глюкозо-6-фосфат" ID="ID_53" GOLD_RELATION="precedes">
        <node TEXT="Фруктозо-6-фосфат" ID="ID_54" GOLD_RELATION="precedes">
          <node TEXT="Фруктозо-1,6-бисфосфат" ID="ID_55" GOLD_RELATION="precedes">
            <node TEXT="Глицеральдегид-3-фосфат" ID="ID_56" GOLD_RELATION="precedes">
              <node TEXT="Пируват" ID="ID_57" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Ферменты" ID="ID_58" GOLD_RELATION="has_part">
      <node TEXT="Гексокиназа" ID="ID_59" GOLD_RELATION="has_example"/>
      <node TEXT="Фосфофруктокиназа" ID="ID_60" GOLD_RELATION="has_example"/>
      <node TEXT="Пируваткиназа" ID="ID_61" GOLD_RELATION="has_example"/>
    </node>
    <node TEXT="Продукты" ID="ID_62" GOLD_RELATION="associated_with">
      <node TEXT="АТФ" ID="ID_63" GOLD_RELATION="causes"/>
      <node TEXT="НАДН" ID="ID_64" GOLD_RELATION="causes"/>
      <node TEXT="Пируват" ID="ID_65" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Свойства" ID="ID_66" GOLD_RELATION="associated_with">
      <node TEXT="Анаэробный процесс" ID="ID_67" GOLD_RELATION="has_property"/>
      <node TEXT="Протекает в цитоплазме" ID="ID_68" GOLD_RELATION="has_property"/>
      <node TEXT="Низкий выход энергии" ID="ID_69" GOLD_RELATION="has_property"/>
    </node>
  </node>
</map>
