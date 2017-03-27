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

from tqdm import tqdm
# from scipy.sparse import coo_matrix

if __name__ == '__main__':
    train_matr, accounts = get_cluster_matrix(sys.argv[1])

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Fit LDA
    lda = fit_and_get_lda(train_matr)
    # Transform account-cluster matrix accoring to fitted LDA
    train_transform = lda.transform(train_matr)
    # Get account-topic matrix from transformed matrix
    acc_top_matrix = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_clus_matrix = get_topic_cluster_matrix(lda.components_)
    # Get map of movie probabilities with clusters
    clus_mov_map = get_cluster_movies_map(sys.argv[1])

    n_transactions = get_line_count(sys.argv[2]) - 1
    testset = get_data_file_pointer(sys.argv[2])
    guess_accuracy_sum = 0
    entries = 0
    zero_p_count = 0
    for trans in tqdm(testset, total=n_transactions):
        u_hash = trans['hashed_ID']
        cluster = trans['KMeans']
        movie = trans['VM_TITLE']
        p = 0

        ## Guess cluster
        if u_hash in acc_top_matrix:
            
            p = sum(t_p * top_clus_matrix[i][int(cluster)]
                for i, t_p in enumerate(acc_top_matrix[u_hash]))

            # Additionally guess movie
            if movie in clus_mov_map[cluster]:
                p *= clus_mov_map[cluster][movie]

        if p == 0:
            zero_p_count += 1
        else:
            guess_accuracy_sum -= math.log(p, 2)
        entries += 1
            
    
    print 'Entropy: {}'.format(guess_accuracy_sum / entries)
    print 'Loss: {}'.format(zero_p_count / n_transactions)

