# Отчёт об обучении: `exp_tfidf`

- backend: **tfidf_logreg**
- per-seed cap: 100
- per-class cap: 300
- test size: 0.25
- use SBERT: False
- random state: 42
- train pairs: **461**, test pairs: **225**
- признаков: **6**

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

- macro-F1:    **0.3386**
- weighted-F1: **0.4448**

### Per-class

| class        |   precision |   recall |     f1 |   support |
|:-------------|------------:|---------:|-------:|----------:|
| causes       |      0.4667 |   0.1892 | 0.2692 |        37 |
| has_example  |      0.6321 |   0.6262 | 0.6291 |       107 |
| has_function |      0.2941 |   0.25   | 0.2703 |        20 |
| has_part     |      0.2917 |   0.3043 | 0.2979 |        23 |
| has_property |      0.2727 |   0.15   | 0.1935 |        20 |
| precedes     |      0.25   |   0.7222 | 0.3714 |        18 |

### Confusion matrix (строки — true, столбцы — pred)

|              |   causes |   has_example |   has_function |   has_part |   has_property |   precedes |
|:-------------|---------:|--------------:|---------------:|-----------:|---------------:|-----------:|
| causes       |        7 |            10 |              1 |          0 |              1 |         18 |
| has_example  |        3 |            67 |              5 |          7 |              5 |         20 |
| has_function |        2 |             8 |              5 |          4 |              0 |          1 |
| has_part     |        0 |            13 |              2 |          7 |              1 |          0 |
| has_property |        2 |             6 |              3 |          6 |              3 |          0 |
| precedes     |        1 |             2 |              1 |          0 |              1 |         13 |
