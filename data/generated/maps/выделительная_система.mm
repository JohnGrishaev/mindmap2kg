<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Выделительная система" ID="ID_267">
    <node TEXT="Почки" ID="ID_268" GOLD_RELATION="has_part">
      <node TEXT="Нефрон" ID="ID_269" GOLD_RELATION="has_part">
        <node TEXT="Почечная капсула" ID="ID_270" GOLD_RELATION="has_part"/>
        <node TEXT="Почечные канальцы" ID="ID_271" GOLD_RELATION="has_part"/>
        <node TEXT="Фильтрация крови" ID="ID_272" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Корковое вещество" ID="ID_273" GOLD_RELATION="has_part"/>
      <node TEXT="Мозговое вещество" ID="ID_274" GOLD_RELATION="has_part"/>
      <node TEXT="Почечная лоханка" ID="ID_275" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Мочеточники" ID="ID_276" GOLD_RELATION="has_part"/>
    <node TEXT="Мочевой пузырь" ID="ID_277" GOLD_RELATION="has_part"/>
    <node TEXT="Мочеиспускательный канал" ID="ID_278" GOLD_RELATION="has_part"/>
    <node TEXT="Образование мочи" ID="ID_279" GOLD_RELATION="associated_with">
      <node TEXT="Фильтрация" ID="ID_280" GOLD_RELATION="has_part">
        <node TEXT="Реабсорбция" ID="ID_281" GOLD_RELATION="precedes">
          <node TEXT="Секреция" ID="ID_282" GOLD_RELATION="precedes"/>
        </node>
      </node>
      <node TEXT="Первичная моча" ID="ID_283" GOLD_RELATION="associated_with"/>
      <node TEXT="Вторичная моча" ID="ID_284" GOLD_RELATION="associated_with"/>
    </node>
    <node TEXT="Другие органы выделения" ID="ID_285" GOLD_RELATION="associated_with">
      <node TEXT="Кожа" ID="ID_286" GOLD_RELATION="has_example">
        <node TEXT="Потовые железы" ID="ID_287" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Легкие" ID="ID_288" GOLD_RELATION="has_example"/>
      <node TEXT="Печень" ID="ID_289" GOLD_RELATION="has_example"/>
    </node>
  </node>
</map>
