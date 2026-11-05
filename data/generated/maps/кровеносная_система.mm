<?xml version='1.0' encoding='UTF-8'?>
<map version="1.0.1">
  <node TEXT="Кровеносная система" ID="ID_39">
    <node TEXT="Сердце" ID="ID_40" GOLD_RELATION="has_part">
      <node TEXT="Предсердия" ID="ID_41" GOLD_RELATION="has_part"/>
      <node TEXT="Желудочки" ID="ID_42" GOLD_RELATION="has_part"/>
      <node TEXT="Клапаны" ID="ID_43" GOLD_RELATION="has_part">
        <node TEXT="Створчатые клапаны" ID="ID_44" GOLD_RELATION="has_example"/>
        <node TEXT="Полулунные клапаны" ID="ID_45" GOLD_RELATION="has_example"/>
      </node>
      <node TEXT="Миокард" ID="ID_46" GOLD_RELATION="has_part"/>
      <node TEXT="Автоматизм" ID="ID_47" GOLD_RELATION="has_property"/>
      <node TEXT="Перекачивание крови" ID="ID_48" GOLD_RELATION="has_function"/>
    </node>
    <node TEXT="Сосуды" ID="ID_49" GOLD_RELATION="has_part">
      <node TEXT="Артерии" ID="ID_50" GOLD_RELATION="has_example">
        <node TEXT="Аорта" ID="ID_51" GOLD_RELATION="has_example"/>
        <node TEXT="Толстые упругие стенки" ID="ID_52" GOLD_RELATION="has_property"/>
      </node>
      <node TEXT="Вены" ID="ID_53" GOLD_RELATION="has_example">
        <node TEXT="Полая вена" ID="ID_54" GOLD_RELATION="has_example"/>
        <node TEXT="Наличие клапанов" ID="ID_55" GOLD_RELATION="has_property"/>
      </node>
      <node TEXT="Капилляры" ID="ID_56" GOLD_RELATION="has_example">
        <node TEXT="Газообмен с тканями" ID="ID_57" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Круги кровообращения" ID="ID_58" GOLD_RELATION="associated_with">
      <node TEXT="Большой круг" ID="ID_59" GOLD_RELATION="has_example">
        <node TEXT="Левый желудочек" ID="ID_60" GOLD_RELATION="associated_with"/>
      </node>
      <node TEXT="Малый круг" ID="ID_61" GOLD_RELATION="has_example">
        <node TEXT="Правый желудочек" ID="ID_62" GOLD_RELATION="associated_with"/>
        <node TEXT="Обогащение крови кислородом" ID="ID_63" GOLD_RELATION="has_function"/>
      </node>
    </node>
    <node TEXT="Сердечный цикл" ID="ID_64" GOLD_RELATION="associated_with">
      <node TEXT="Систола предсердий" ID="ID_65" GOLD_RELATION="has_part">
        <node TEXT="Систола желудочков" ID="ID_66" GOLD_RELATION="precedes">
          <node TEXT="Общая диастола" ID="ID_67" GOLD_RELATION="precedes"/>
        </node>
      </node>
    </node>
  </node>
</map>
