import sys
import numpy as np
import sklearn.decomposition as dec
sys.path.insert(0, '../../00-common')
from common import get_data_file_pointer

from tqdm import tqdm
from scipy.sparse import coo_matrix

accounts = {}
n_clusters = -1

if __name__ == '__main__':
    # create the sparse matrix
    csvfile = get_data_file_pointer(sys.argv[1])

    print 'Creating the hashmaps for accounts indexes'
    for transact in tqdm(csvfile, total=2576791):
        if transact['hashed_ID'] not in accounts:
            accounts[transact['hashed_ID']] = len(accounts)

        if int(transact['KMeans']) > n_clusters:
            n_clusters = int(transact['KMeans'])

    n_clusters += 1
    print 'n_clusters ' + str(n_clusters)

    col = []
    row = []

    csvfile = get_data_file_pointer(sys.argv[1])

    print 'creating the rows and cols lists'
    for transact in tqdm(csvfile, total=2576791):
        row.append(accounts[transact['hashed_ID']])
        col.append(int(transact['KMeans']))

    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(len(accounts), n_clusters))

    print matr.todense()

    lda = dec.LatentDirichletAllocation(n_topics=30, n_jobs=-1, learning_method='batch', verbose=3, max_iter=1)

    print 'lda creates, starting fit'

    lda.fit(matr)

    print 'fit finished'

    print lda
    print lda.components_

    transformed = lda.transform(matr)
    micro_cands = []

    for topics_dist in transformed:
        good_nums = 0
        for num in topics_dist:
            if num >= 0.1:
                good_nums = good_nums + 1
        if good_nums > 1:
            micro_cands.append(topics_dist)
            print good_nums

    print "Accounts: {}".format(len(accounts))
    print "Micro-profile cands.: {}".format(len(micro_cands))

    # model = lda
    # feature_names = ['year', 'hour', 'day']
    # n_top_words = 20
    # for topic_idx, topic in enumerate(model.components_):
    #     print("Topic #%d:" % topic_idx)
    #     print(" ".join([feature_names[i]
    #                     for i in topic.argsort()[:-n_top_words - 1:-1]]))
    # print()
