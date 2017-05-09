# micro-profiling

## Evaluation
We have some different datasets we have tested on (or rather different portions of the whole), with all transactions of tv-series pruned:
1. <a name="d1"></a> Sorted by most active users we used transactions from 10% (80 to 90 percentiles).
2. <a name="d2"></a> Sorted by most active users we used transactions from 10% (87 to 97 percentiles). The reason for the higher percentiles is due to the cleaning done to this set, i.e. identical movie-transactions appearing close together in time have been reduced to just one transaction.

### Cross-validation using separate train and test sets
#### Guessing individual movie
|           Model            |  LDA (topics)  | Entropy[[1]](#d1) | Loss[[1]](#d1) | Entropy[[2]](#d2) | Loss[[2]](#d2) |
| -------------------------- | :------------: | :---------------: | :------------: | :---------------: | :------------: |
| Genre (as sets)            |                | 8.0               | 14 %           | 8.92              | 25 %           |
| Genre (as sets)            | 10             | 9.46              |                | 9.94              |                |
| Genre + Time intervals     |                | 7.83              | 22 %           | 8.61              | 52 %           |
| Clustering (100 clusters)  |                | 7.5               | 9.8 %          |                   |                |
| Clustering (40 clusters)   |                | 8.18              | 5.3 %          | 8.71              | 7 %            |
| Clustering (40 clusters)   | 10             | 8.92              |                | 9.38              |                |

#### Guessing group (e.g. cluster or genre)
|           Model            |  LDA (topics)  | Entropy[[1]](#d1) | Loss[[1]](#d1) |
| -------------------------- | :------------: | :---------------: | :------------: |
| Genre (as sets)            | 10             | 4.12              |                |


### Cross-validation with same data set as train and test (MDL purposes)
#### Guessing individual movie
|           Model            |  LDA (topics) | Entropy[[1]](#d1) | Entropy[[2]](#d2) |
| -------------------------- | :-----------: | :---------------: | :---------------: |
| Frequency/popularity       |               | 10.35             | 10.72             |

#### Guessing group (e.g. cluster or genre)
|           Model            |  LDA (topics) | Entropy[[1]](#d1) | Entropy[[2]](#d2) |
| -------------------------- | :-----------: | :---------------: | :---------------: |
| Genre (as sets)            | 10            | 3.89              | 4.03              |
| Genre (as sets)            |               | 1.83              | 2.14              |
| Clustering (40 clusters)   | 10            | 2.26              | 2.48              |
| Clustering (40 clusters)   | 30            | 2.37              |                   |
| Clustering (40 clusters)   |               | 1.12              |                   |



## Recall@k

### 10p_clean_w_clusters (no accounts division)
| model | k=10 | k=20 | k=50|
|---|---|---|---|
|Frequency| 0.04268733806426925| 0.07817847410068222| 0.16544932762018003|
|genre baseline| 0.08813351998105613| 0.15798747476646555| 0.29117978228825936|
|personalised genre| 0.10289447098300475| 0.1689393116100391| 0.29586199165923693|
|LDA 10 topics| 0.11809149058873507| 0.19559071735379904| 0.34780468685834587|
|LDA 40 topics| 0.14546553163219608| 0.23621379285292846| 0.4022641725785127|
|LDA 100 topics| 0.157819953478631| 0.2529336200695389| 0.42488552632142723|
|LDA 40 topics 100 clusters| 0.07485962490975234| 0.13140749623665895| 0.25836414151354553|

### 10p_clean_w_clusters_divided_sort (divided by time)

| model | k=10 | k=20 | k=50|
|---|---|---|---|
|Frequency | 0.04763603727248128 | 0.08471325365560174 | 0.17278276206187915|
|genre baseline | 0.0999709325693116 | 0.1609774988305846| 0.2715234461372083|
|personalised genre | 0.10397630372757262| 0.16544945865636423| 0.2757338849610023|
|LDA 10 topics | 0.12373954579187893| 0.20122276270695386| 0.3467353352162765|
|LDA 40 topics | 0.152959307627251| 0.23796164019280827| 0.38611444113928295|
|LDA 40 topics 40 clusters| 0.0913275113176356| 0.15251402483896953| 0.2796972104573891|
|LDA 40 topics 100 clusters|0.0993187062354003| 0.1631180938027221| 0.29563547443624855|


_____________________________
not usefull
### 10p_clean_w_clusters_w_topics (divided by LDA 40 topics)
| model | k=10 | k=20 | k=50|
|---|---|---|---|
|Frequency| 0.04074010348996031| 0.07770936270343574| 0.16497236262785778|
|personalised genre| 0.15483145267522289| 0.23792093136739675| 0.3762470203178532|




