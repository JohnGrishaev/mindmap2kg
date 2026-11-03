# Отчёт об обучении: `exp_logreg_sbert`

- backend: **logreg**
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

- macro-F1:    **0.2567**
- weighted-F1: **0.2868**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |       0.75  |   0.2    | 0.3158 |        15 |
| has_example  |       1     |   0.2097 | 0.3467 |        62 |
| has_function |       0.125 |   0.5    | 0.2    |         8 |
| has_part     |       0.175 |   0.35   | 0.2333 |        20 |
| has_property |       0.15  |   0.25   | 0.1875 |        24 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|
| causes       |        3 |             0 |              2 |          4 |              6 |
| has_example  |        0 |            13 |             17 |         13 |             19 |
| has_function |        0 |             0 |              4 |          1 |              3 |
| has_part     |        1 |             0 |              6 |          7 |              6 |
| has_property |        0 |             0 |              3 |         15 |              6 |
