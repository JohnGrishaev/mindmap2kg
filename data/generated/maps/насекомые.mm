<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Насекомые" ID="ID_32">
    <node TEXT="Строение" ID="ID_33" GOLD_RELATION="associated_with">
      <node TEXT="Голова" ID="ID_34" GOLD_RELATION="has_part">
        <node TEXT="Усики" ID="ID_35" GOLD_RELATION="has_part"/>
        <node TEXT="Сложные глаза" ID="ID_36" GOLD_RELATION="has_part"/>
        <node TEXT="Ротовой аппарат" ID="ID_37" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Грудь" ID="ID_38" GOLD_RELATION="has_part">
        <node TEXT="Три пары ног" ID="ID_39" GOLD_RELATION="has_part"/>
        <node TEXT="Крылья" ID="ID_40" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Брюшко" ID="ID_41" GOLD_RELATION="has_part">
        <node TEXT="Трахеи" ID="ID_42" GOLD_RELATION="has_part">
          <node TEXT="Дыхание" ID="ID_43" GOLD_RELATION="has_function"/>
        </node>
      </node>
      <node TEXT="Хитиновый покров" ID="ID_44" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Развитие" ID="ID_45" GOLD_RELATION="associated_with">
      <node TEXT="С полным превращением" ID="ID_46" GOLD_RELATION="has_example">
        <node TEXT="Яйцо" ID="ID_47" GOLD_RELATION="has_part">
          <node TEXT="Личинка" ID="ID_48" GOLD_RELATION="precedes">
            <node TEXT="Куколка" ID="ID_49" GOLD_RELATION="precedes">
              <node TEXT="Взрослое насекомое" ID="ID_50" GOLD_RELATION="precedes"/>
            </node>
          </node>
        </node>
        <node TEXT="Бабочки" ID="ID_51" GOLD_RELATION="has_example"/>
        <node TEXT="Жуки" ID="ID_52" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="С неполным превращением" ID="ID_53" GOLD_RELATION="has_example">
        <node TEXT="Яйцо" ID="ID_54" GOLD_RELATION="has_part">
          <node TEXT="Личинка" ID="ID_55" GOLD_RELATION="precedes">
            <node TEXT="Взрослое насекомое" ID="ID_56" GOLD_RELATION="precedes"/>
          </node>
        </node>
        <node TEXT="Кузнечики" ID="ID_57" GOLD_RELATION="has_example"/>
        <node TEXT="Стрекозы" ID="ID_58" GOLD_RELATION="has_example"/>
      </node>
    </node>
    <node TEXT="Значение" ID="ID_59" GOLD_RELATION="associated_with">
      <node TEXT="Опыление растений" ID="ID_60" GOLD_RELATION="has_function"/>
      <node TEXT="Переносчики болезней" ID="ID_61" GOLD_RELATION="has_function">
        <node TEXT="Малярийный комар" ID="ID_62" GOLD_RELATION="has_example">
          <node TEXT="Малярия" ID="ID_63" GOLD_RELATION="causes"/>
        </node>
      </node>
    </node>
  </node>
</map>
