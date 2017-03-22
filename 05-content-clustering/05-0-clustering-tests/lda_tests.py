import sys
import numpy as np
import sklearn.decomposition as dec
from sklearn.preprocessing import normalize
sys.path.insert(0, '../../00-common')
from common import get_data_file_pointer

from tqdm import tqdm
from scipy.sparse import coo_matrix

accounts = {}
n_clusters = -1
min_topic_p = 0.1

if __name__ == '__main__':
    # create the sparse matrix
    csvfile = get_data_file_pointer(sys.argv[1])

    print 'Creating the hashmaps for accounts indexes'
    for transact in tqdm(csvfile, total=2576791):
        if transact['hashed_ID'] not in accounts:
            accounts[transact['hashed_ID']] = len(accounts)

        if int(transact['KMeans']) > n_clusters:
            n_clusters = int(transact['KMeans'])

    # Populate inv_accounts
    inv_accounts = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        inv_accounts[i] = u_hash

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
    # Normalize: 'l1' = each row sums to 1
    matr = normalize(matr, axis=1, norm='l1')

    print matr.todense()

    lda = dec.LatentDirichletAllocation(n_topics=30, n_jobs=-1, learning_method='batch', verbose=3, max_iter=1)

    print 'lda created, starting fit'

    lda.fit(matr)

    print 'fit finished'

    # print lda
    # print lda.components_

    transformed = lda.transform(matr)
    micro_cands = {}

    for i, topics_dist in enumerate(transformed):
        good_nums = 0
        for num in topics_dist:
            if num >= min_topic_p:
                good_nums = good_nums + 1
        if good_nums > 1:
            micro_cands[inv_accounts[i]] = topics_dist
            #print good_nums

    print "Accounts: {}".format(len(accounts))
    print "Micro-profile cands.: {}".format(len(micro_cands))

    for topic in transformed.dot(normalize(lda.components_, axis=1, norm='l1')):
        print "{} {}".format(sum(topic), topic)

    for u_hash, topic_dist in micro_cands.iteritems():
        topics = []
        for i, p in enumerate(topic_dist):
            if p >= min_topic_p:
                topics.append("{:>2}: {:>6.4}".format(i, p))
        print "{} {}".format(u_hash, topics)

    #
    
    #print transformed.dot(normalize(lda.components_, axis=1, norm='l1'))

    #print 'First candidate'


    
