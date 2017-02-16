# Genre Model
## Model Output
This model produces two probability tables. One table with each user's genre distribution and one table with each genre's movie distribution.

### Table 1: User - Genre Table
For each user *i* we have a row in the table and the probabilities *p_i* of each genre set from the movies user *i* has watched:

| User | p(drama, action) | p(kids, animation) |
| ---- | :--------------: | :----------------: |
| U*1* | 0.23             | 0.4221             |
| U*2* | 0.02             | 0.654              |
| ...  | ...              | ...                |
| U*n* | x                | y                  |

### Table 2: Genre - Movie Table
For each genre set *j* (as above) we have a row in the table and the probabilities *q_x* of a movie appearing in that set:

| Genre set | p(The Matrix (1999)) | p(Jaws (1975)) |
| --------- | :------------------: | :------------: |
| G*1*      | 0.056                | 0.0014         |
| G*2*      | 0.0001               | 0.0            |
| ...       | ...                  | ...            |
| G*m*      | x                    | y              |

The internal representation of the tables are arbitrary. Since it might not make sense to store a "0.0" probability about a movie, a hashtable could be used for each row instead.

## Calculating entropy
After the two above tables have been created from the whole dataset, the entropy can be calculated by getting the probability of each transaction from the dataset.
The probability of transaction *k* appearing in the dataset is calculated as

*p_i* * *q_x*,

where *p_i* is the probability of the genre set from *k* appearing in the set of genres for the user *i* from *k*, and *q_x* is the probability of movie *x* from *k* appearing in the same genre set.
