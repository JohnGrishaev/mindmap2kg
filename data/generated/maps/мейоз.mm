<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Мейоз" ID="ID_43">
    <node TEXT="Мейоз I" ID="ID_44" GOLD_RELATION="has_part">
      <node TEXT="Профаза I" ID="ID_45" GOLD_RELATION="has_part">
        <node TEXT="Лептотена" ID="ID_46" GOLD_RELATION="has_part">
          <node TEXT="Зиготена" ID="ID_47" GOLD_RELATION="precedes">
            <node TEXT="Пахитена" ID="ID_48" GOLD_RELATION="precedes">
              <node TEXT="Диплотена" ID="ID_49" GOLD_RELATION="precedes">
                <node TEXT="Диакинез" ID="ID_50" GOLD_RELATION="precedes"/>
              </node>
            </node>
          </node>
        </node>
        <node TEXT="Конъюгация гомологичных хромосом" ID="ID_51" GOLD_RELATION="has_part"/>
        <node TEXT="Кроссинговер" ID="ID_52" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Метафаза I" ID="ID_53" GOLD_RELATION="has_part"/>
      <node TEXT="Анафаза I" ID="ID_54" GOLD_RELATION="has_part">
        <node TEXT="Расхождение гомологичных хромосом" ID="ID_55" GOLD_RELATION="has_part"/>
      </node>
      <node TEXT="Телофаза I" ID="ID_56" GOLD_RELATION="has_part"/>
    </node>
    <node TEXT="Мейоз II" ID="ID_57" GOLD_RELATION="has_part">
      <node TEXT="Профаза II" ID="ID_58" GOLD_RELATION="has_part">
        <node TEXT="Метафаза II" ID="ID_59" GOLD_RELATION="precedes">
          <node TEXT="Анафаза II" ID="ID_60" GOLD_RELATION="precedes">
            <node TEXT="Телофаза II" ID="ID_61" GOLD_RELATION="precedes"/>
          </node>
        </node>
      </node>
    </node>
    <node TEXT="Результат" ID="ID_62" GOLD_RELATION="associated_with">
      <node TEXT="Четыре гаплоидные клетки" ID="ID_63" GOLD_RELATION="causes"/>
      <node TEXT="Комбинативная изменчивость" ID="ID_64" GOLD_RELATION="causes"/>
    </node>
    <node TEXT="Значение" ID="ID_65" GOLD_RELATION="associated_with">
      <node TEXT="Образование гамет" ID="ID_66" GOLD_RELATION="has_function"/>
      <node TEXT="Постоянство кариотипа вида" ID="ID_67" GOLD_RELATION="has_function"/>
    </node>
  </node>
</map>
