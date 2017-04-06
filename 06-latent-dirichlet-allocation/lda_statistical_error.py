import sys
import math
# import numpy as np
# import sklearn.decomposition as dec
# from sklearn.preprocessing import normalize
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
# from lda import get_cluster_matrix
from lda import get_term_movie_matrix
from lda import fit_and_get_lda
from lda import get_account_topic_matrix
from lda import get_topic_cluster_matrix
from lda import get_user_movie_matrix

from sklearn.preprocessing import normalize

from tqdm import tqdm
# from scipy.sparse import coo_matrix

if __name__ == '__main__':
    train_matr, accounts, movie_by_index = get_user_movie_matrix(sys.argv[1])

    lda = fit_and_get_lda(train_matr, 40, 10)
    doc_topic_distr = lda.transform(train_matr)
    topic_term_distr = lda.components_

    # topic_term_distr = normalize(topic_term_distr, axis=1, norm='l1')
    # print topic_term_distr.sum(axis=1)

    print doc_topic_distr[3]
    for document in xrange(len(doc_topic_distr)):
        doc_topic_distr[document] = [t if t > (1.0/20) else 0 for t in doc_topic_distr[document]]

    print doc_topic_distr[3]


    computed_input_matrix = doc_topic_distr.dot(topic_term_distr)
    computed_input_matrix = normalize(computed_input_matrix, axis=1, norm='l1')

    train_matr = normalize(train_matr, axis=1, norm='l1')

    # print computed_input_matrix
    # print train_matr.todense()

    train_matr = train_matr.todense()
    line_diff = []
    for i in xrange(len(computed_input_matrix)):
        original = train_matr[i].flatten().tolist()[0]
        computed = computed_input_matrix[i]

        line_diff.append(sum([abs(x[0] - x[1]) for x in zip(original, computed)]))

    print sum(line_diff) / len(line_diff) / 2
