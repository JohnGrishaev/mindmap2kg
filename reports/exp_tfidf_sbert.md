# Отчёт об обучении: `exp_tfidf_sbert`

- backend: **tfidf_logreg**
- per-seed cap: 100
- per-class cap: 300
- test size: 0.25
- use SBERT: True, full vectors: True
- random state: 42
- train pairs: **461**, test pairs: **225**
- признаков: **1545**

## Распределение классов в обучении

|              |   count |
|:-------------|--------:|
| precedes     |     123 |
| has_part     |      90 |
| has_example  |     300 |
| causes       |      86 |
| has_property |      52 |
| has_function |      35 |

## Метрики

- macro-F1:    **0.3701**
- weighted-F1: **0.4279**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.4737 |   0.2432 | 0.3214 |        37 |
| has_example  |      0.5625 |   0.5047 | 0.532  |       107 |
| has_function |      0.2778 |   0.25   | 0.2632 |        20 |
| has_part     |      0.3077 |   0.3478 | 0.3265 |        23 |
| has_property |      0.4    |   0.3    | 0.3429 |        20 |
| precedes     |      0.2941 |   0.8333 | 0.4348 |        18 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |   precedes |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|-----------:|
| causes       |        9 |            10 |              0 |          1 |              2 |         15 |
| has_example  |        7 |            54 |             10 |         13 |              4 |         19 |
| has_function |        2 |             7 |              5 |          2 |              2 |          2 |
| has_part     |        0 |            12 |              2 |          8 |              1 |          0 |
| has_property |        1 |            11 |              1 |          1 |              6 |          0 |
| precedes     |        0 |             2 |              0 |          1 |              0 |         15 |
