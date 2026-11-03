# Отчёт об обучении: `exp_gbm_sbert`

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

- macro-F1:    **0.2892**
- weighted-F1: **0.3858**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.3846 |   0.3333 | 0.3571 |        15 |
| has_example  |      0.5469 |   0.5645 | 0.5556 |        62 |
| has_function |      0.125  |   0.125  | 0.125  |         8 |
| has_part     |      0.1786 |   0.25   | 0.2083 |        20 |
| has_property |      0.25   |   0.1667 | 0.2    |        24 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|
| causes       |        5 |             6 |              0 |          1 |              3 |
| has_example  |        5 |            35 |              3 |         12 |              7 |
| has_function |        0 |             3 |              1 |          4 |              0 |
| has_part     |        3 |             9 |              1 |          5 |              2 |
| has_property |        0 |            11 |              3 |          6 |              4 |
