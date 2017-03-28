# micro-profiling
blah

## Cross-validation using separate train and test sets
### Guessing individual movie
|           Model            |  LDA (topics)  | Entropy | Loss    |
| -------------------------- | :------------: | :-----: | :-----: |
| Frequency/popularity       |                | 10.35   | Unknown |
| Genre (as sets)            |                | 8.0     | 14 %    |
| Genre (as sets)            | 10             | 9.46    |         |
| Genre + Time intervals     |                | 7.83    | 22 %    |
| Clustering (100 clusters)  |                | 7.5     | 9.8 %   |
| Clustering (40 clusters)   |                | 8.18    | 5.3 %   |

### Guessing group (e.g. cluster or genre)
|           Model            |  LDA (topics)  | Entropy | Loss    |
| -------------------------- | :------------: | :-----: | :-----: |
| Genre (as sets)            | 10             | 4.12    |         |


## Cross-validation with same data set as train and test (MDL purposes)
|           Model            |  LDA (topics) | Entropy |
| -------------------------- | :-----------: | :-----: |
| Genre (as sets)            | 10            | 3.89    |
| Genre (as sets)            |               | 1.83    |
| Clustering (40 clusters)   | 10            | 2.26    |
| Clustering (40 clusters)   | 30            | 2.37    |
| Clustering (40 clusters)   |               | 1.12    |
