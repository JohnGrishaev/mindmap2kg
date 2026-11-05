<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Эндокринная система" ID="ID_176">
    <node TEXT="Гипофиз" ID="ID_177" GOLD_RELATION="has_part">
      <node TEXT="Гормон роста" ID="ID_178" GOLD_RELATION="has_part">
        <node TEXT="Рост организма" ID="ID_179" GOLD_RELATION="has_function"/>
        <node TEXT="Гигантизм" ID="ID_180" GOLD_RELATION="associated_with"/>
        <node TEXT="Карликовость" ID="ID_181" GOLD_RELATION="associated_with"/>
      </node>
      <node TEXT="Главная железа" ID="ID_182" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Щитовидная железа" ID="ID_183" GOLD_RELATION="has_part">
      <node TEXT="Тироксин" ID="ID_184" GOLD_RELATION="has_part">
        <node TEXT="Регуляция обмена веществ" ID="ID_185" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Недостаток йода" ID="ID_186" GOLD_RELATION="associated_with"/>
    </node>
    <node TEXT="Надпочечники" ID="ID_187" GOLD_RELATION="has_part">
      <node TEXT="Адреналин" ID="ID_188" GOLD_RELATION="has_part">
        <node TEXT="Учащение сердцебиения" ID="ID_189" GOLD_RELATION="causes"/>
        <node TEXT="Повышение уровня глюкозы" ID="ID_190" GOLD_RELATION="causes"/>
      </node>
    </node>
    <node TEXT="Поджелудочная железа" ID="ID_191" GOLD_RELATION="has_part">
      <node TEXT="Инсулин" ID="ID_192" GOLD_RELATION="has_part">
        <node TEXT="Снижение уровня глюкозы" ID="ID_193" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Глюкагон" ID="ID_194" GOLD_RELATION="has_part">
        <node TEXT="Повышение уровня глюкозы" ID="ID_195" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Половые железы" ID="ID_196" GOLD_RELATION="has_part">
      <node TEXT="Тестостерон" ID="ID_197" GOLD_RELATION="has_part"/>
      <node TEXT="Эстроген" ID="ID_198" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Свойства гормонов" ID="ID_199" GOLD_RELATION="associated_with">
      <node TEXT="Высокая биологическая активность" ID="ID_200" GOLD_RELATION="has_property"/>
      <node TEXT="Специфичность действия" ID="ID_201" GOLD_RELATION="has_property"/>
      <node TEXT="Дистанционность" ID="ID_202" GOLD_RELATION="has_property"/>
    </node>
  </node>
</map>
