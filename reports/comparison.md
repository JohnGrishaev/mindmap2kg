# Сравнение прогонов

| run_id           | backend   | use_sbert   |   n_features |   n_train |   n_test |   macro_f1 |   weighted_f1 |
|:-----------------|:----------|:------------|-------------:|----------:|---------:|-----------:|--------------:|
| exp_rf_sbert     | rf        | True        |           10 |       463 |      225 |     0.4069 |        0.485  |
| exp_gbm_sbert    | gbm       | True        |           10 |       463 |      225 |     0.3831 |        0.4528 |
| exp_logreg_sbert | logreg    | True        |           10 |       463 |      225 |     0.2281 |        0.2088 |
