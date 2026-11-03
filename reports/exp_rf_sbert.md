# Отчёт об обучении: `exp_rf_sbert`

- backend: **rf**
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

- macro-F1:    **0.3071**
- weighted-F1: **0.4122**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.4615 |   0.4    | 0.4286 |        15 |
| has_example  |      0.6066 |   0.5968 | 0.6016 |        62 |
| has_function |      0.0909 |   0.125  | 0.1053 |         8 |
| has_part     |      0.2143 |   0.3    | 0.25   |        20 |
| has_property |      0.1875 |   0.125  | 0.15   |        24 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|
| causes       |        6 |             4 |              1 |          0 |              4 |
| has_example  |        5 |            37 |              4 |         10 |              6 |
| has_function |        1 |             2 |              1 |          4 |              0 |
| has_part     |        1 |             8 |              2 |          6 |              3 |
| has_property |        0 |            10 |              3 |          8 |              3 |
