# Отчёт об обучении: `exp_maps`

- backend: **tfidf_logreg**
- per-seed cap: 0
- per-class cap: 0
- test size: 0.25
- use SBERT: False, full vectors: False
- random state: 42
- train pairs: **1222**, test pairs: **395**
- признаков: **16**

## Распределение классов в обучении

|              |   count |
|:-------------|--------:|
| causes       |     130 |
| has_property |     141 |
| has_example  |     579 |
| has_part     |     434 |
| precedes     |     131 |
| has_function |     202 |

## Метрики

- macro-F1:    **0.6817**
- weighted-F1: **0.6875**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.42   |   0.4884 | 0.4516 |        43 |
| has_example  |      0.8468 |   0.7015 | 0.7673 |       134 |
| has_function |      0.7222 |   0.6393 | 0.6783 |        61 |
| has_part     |      0.6071 |   0.701  | 0.6507 |        97 |
| has_property |      0.6667 |   0.7179 | 0.6914 |        39 |
| precedes     |      0.7692 |   0.9524 | 0.8511 |        21 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |   precedes |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|-----------:|
| causes       |       21 |             1 |              6 |          9 |              3 |          3 |
| has_example  |       11 |            94 |              3 |         22 |              4 |          0 |
| has_function |       11 |             0 |             39 |          9 |              2 |          0 |
| has_part     |        5 |            14 |              2 |         68 |              5 |          3 |
| has_property |        2 |             2 |              4 |          3 |             28 |          0 |
| precedes     |        0 |             0 |              0 |          1 |              0 |         20 |
