# micro-profiling
blah

## Evaluation
We have some different datasets we have tested on (or rather different portions of the whole), with all transactions of tv-series pruned:
1. Sorted by most active users we used transactions from 10% (80 to 90 percentiles). <a name="d1"></a>
2. Sorted by most active users we used transactions from 10% (87 to 97 percentiles). The reason for the higher percentiles is due to the cleaning done to this set, i.e. identical movie-transactions appearing close together in time have been reduced to just one transaction. <a name="d2"></a>

### Cross-validation using separate train and test sets
#### Guessing individual movie
|           Model            |  LDA (topics)  | Entropy[[1]](#d1) | Loss[[1]](#d1) | Entropy[[2]](#d2) | Loss[[2]](#d2) |
| -------------------------- | :------------: | :---------------: | :------------: | :---------------: | :------------: |
| Genre (as sets)            |                | 8.0               | 14 %           | 8.92              | 25 %           |
| Genre (as sets)            | 10             | 9.46              |                | 9.94              |                |
| Genre + Time intervals     |                | 7.83              | 22 %           | 8.61              | 52 %           |
| Clustering (100 clusters)  |                | 7.5               | 9.8 %          |                   |                |
| Clustering (40 clusters)   |                | 8.18              | 5.3 %          |                   |                |
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
