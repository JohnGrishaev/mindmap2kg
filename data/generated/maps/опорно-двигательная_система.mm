<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Опорно-двигательная система" ID="ID_235">
    <node TEXT="Скелет" ID="ID_236" GOLD_RELATION="has_part">
      <node TEXT="Череп" ID="ID_237" GOLD_RELATION="has_part"/>
      <node TEXT="Позвоночник" ID="ID_238" GOLD_RELATION="has_part">
        <node TEXT="Шейный отдел" ID="ID_239" GOLD_RELATION="has_part"/>
        <node TEXT="Грудной отдел" ID="ID_240" GOLD_RELATION="has_part"/>
        <node TEXT="Поясничный отдел" ID="ID_241" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Грудная клетка" ID="ID_242" GOLD_RELATION="has_part"/>
      <node TEXT="Скелет конечностей" ID="ID_243" GOLD_RELATION="has_part"/>
      <node TEXT="Опора" ID="ID_244" GOLD_RELATION="has_function"/>
      <node TEXT="Защита внутренних органов" ID="ID_245" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Кость" ID="ID_246" GOLD_RELATION="associated_with">
      <node TEXT="Надкостница" ID="ID_247" GOLD_RELATION="has_part">
        <node TEXT="Рост кости в толщину" ID="ID_248" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Компактное вещество" ID="ID_249" GOLD_RELATION="has_part"/>
      <node TEXT="Губчатое вещество" ID="ID_250" GOLD_RELATION="has_part">
        <node TEXT="Красный костный мозг" ID="ID_251" GOLD_RELATION="has_part">
          <node TEXT="Кроветворение" ID="ID_252" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Прочность" ID="ID_253" GOLD_RELATION="has_property"/>
      <node TEXT="Упругость" ID="ID_254" GOLD_RELATION="has_property"/>
    </node>
    <node TEXT="Мышцы" ID="ID_255" GOLD_RELATION="has_part">
      <node TEXT="Скелетные мышцы" ID="ID_256" GOLD_RELATION="has_example">
        <node TEXT="Сгибатели" ID="ID_257" GOLD_RELATION="has_example"/>
        <node TEXT="Разгибатели" ID="ID_258" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Гладкие мышцы" ID="ID_259" GOLD_RELATION="has_example"/>
      <node TEXT="Сердечная мышца" ID="ID_260" GOLD_RELATION="has_example"/>
      <node TEXT="Сократимость" ID="ID_261" GOLD_RELATION="has_property"/>
      <node TEXT="Движение" ID="ID_262" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Нарушения осанки" ID="ID_263" GOLD_RELATION="associated_with">
      <node TEXT="Сколиоз" ID="ID_264" GOLD_RELATION="has_example"/>
      <node TEXT="Плоскостопие" ID="ID_265" GOLD_RELATION="has_example"/>
      <node TEXT="Малоподвижный образ жизни" ID="ID_266" GOLD_RELATION="associated_with"/>
    </node>
  </node>
</map>
