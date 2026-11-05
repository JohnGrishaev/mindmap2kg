<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Ухо" ID="ID_39">
    <node TEXT="Наружное ухо" ID="ID_40" GOLD_RELATION="has_part">
      <node TEXT="Ушная раковина" ID="ID_41" GOLD_RELATION="has_part"/>
      <node TEXT="Слуховой проход" ID="ID_42" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Среднее ухо" ID="ID_43" GOLD_RELATION="has_part">
      <node TEXT="Барабанная перепонка" ID="ID_44" GOLD_RELATION="has_part"/>
      <node TEXT="Молоточек" ID="ID_45" GOLD_RELATION="has_part"/>
      <node TEXT="Наковальня" ID="ID_46" GOLD_RELATION="has_part"/>
      <node TEXT="Стремечко" ID="ID_47" GOLD_RELATION="has_part"/>
      <node TEXT="Усиление звука" ID="ID_48" GOLD_RELATION="has_function"/>
      <node TEXT="Евстахиева труба" ID="ID_49" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Внутреннее ухо" ID="ID_50" GOLD_RELATION="has_part">
      <node TEXT="Улитка" ID="ID_51" GOLD_RELATION="has_part">
        <node TEXT="Восприятие звука" ID="ID_52" GOLD_RELATION="has_function"/>
      </node>
      <node TEXT="Вестибулярный аппарат" ID="ID_53" GOLD_RELATION="has_part">
        <node TEXT="Равновесие" ID="ID_54" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Громкий шум" ID="ID_55" GOLD_RELATION="associated_with">
      <node TEXT="Тугоухость" ID="ID_56" GOLD_RELATION="causes"/>
    </node>
  </node>
</map>
