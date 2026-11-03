# Отчёт об обучении: `exp_baseline_gbm`

- backend: **gbm**
- per-seed cap: 100
- per-class cap: 300
- test size: 0.25
- use SBERT: True
- random state: 42
- train pairs: **429**, test pairs: **129**
- признаков: **9**

## Распределение классов в обучении

|              |   count |
|:-------------|--------:|
| has_part     |      82 |
| has_example  |     300 |
| has_property |      55 |
| has_function |      35 |
| causes       |      86 |

## Метрики

- macro-F1:    **0.2973**
- weighted-F1: **0.4025**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.3846 |   0.3333 | 0.3571 |        15 |
| has_example  |      0.5758 |   0.6129 | 0.5938 |        62 |
| has_function |      0.1429 |   0.125  | 0.1333 |         8 |
| has_part     |      0.2    |   0.3    | 0.24   |        20 |
| has_property |      0.2308 |   0.125  | 0.1622 |        24 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|
| causes       |        5 |             5 |              0 |          3 |              2 |
| has_example  |        5 |            38 |              2 |         11 |              6 |
| has_function |        0 |             3 |              1 |          4 |              0 |
| has_part     |        3 |             8 |              1 |          6 |              2 |
| has_property |        0 |            12 |              3 |          6 |              3 |
