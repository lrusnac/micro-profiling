import sys
import math
# import numpy as np
# import sklearn.decomposition as dec
# from sklearn.preprocessing import normalize
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from lda import get_cluster_matrix
from lda import get_cluster_movies_map
from lda import fit_and_get_lda
from lda import get_account_topic_matrix
from lda import get_topic_cluster_matrix

from sklearn.preprocessing import normalize

from tqdm import tqdm
# from scipy.sparse import coo_matrix

if __name__ == '__main__':
    train_matr, accounts = get_cluster_matrix(sys.argv[1])

    lda = fit_and_get_lda(train_matr)
    doc_topic_distr = lda.transform(train_matr)
    topic_term_distr = lda.components_

    # topic_term_distr = normalize(topic_term_distr, axis=1, norm='l1')
    # print topic_term_distr.sum(axis=1)

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

    print sum(line_diff) / len(line_diff)
