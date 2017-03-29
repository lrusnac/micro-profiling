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

    # normalize(topic_term_distr, axis=1, norm='l1')
    topic_term_distr.sum(axis=1)

