import sys
import numpy as np
import sklearn.decomposition as dec
from sklearn.preprocessing import normalize
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

from tqdm import tqdm
from scipy.sparse import coo_matrix

from PIL import Image

n_clusters = -1
lda_max_iter = 10
n_topics = 30
min_topic_p = 0.05

def get_cluster_matrix(filepath):
    csvfile = get_data_file_pointer(filepath)

    ##### Remember index of each account (i.e. which order they appear in the transactions)
    # print 'Creating the hashmaps for accounts indexes'
    accounts = {}
    global n_clusters
    for transact in tqdm(csvfile, total=get_line_count(filepath)):
        if transact['hashed_ID'] not in accounts:
            accounts[transact['hashed_ID']] = len(accounts)

        if int(transact['KMeans']) > n_clusters:
            n_clusters = int(transact['KMeans'])

    n_clusters += 1
    #print 'n_clusters ' + str(n_clusters)

    col = []
    row = []

    csvfile = get_data_file_pointer(filepath)

    ##### Populate matrix: each transaction adds one to (hashed_ID, KMeans)
    #print 'creating the rows and cols lists'
    for transact in tqdm(csvfile, total=get_line_count(filepath)):
        row.append(accounts[transact['hashed_ID']])
        col.append(int(transact['KMeans']))

    ##### Sparse matrix
    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(len(accounts), n_clusters))
    return (matr, accounts)

def get_cluster_movies_map(filepath):
    csvfile = get_data_file_pointer(filepath)
    clusters = {}
    clusters_count = {}

    for trans in tqdm(csvfile, total=get_line_count(filepath)):
        cluster = trans['KMeans']
        movie = trans['VM_TITLE']

        # Initialize/add movie list and count for cluster
        if cluster not in clusters:
            clusters[cluster] = {}
            clusters_count[cluster] = 1
        else:
            clusters_count[cluster] += 1
        
        # Initialize/add movie's count in cluster
        if movie not in clusters[cluster]:
            clusters[cluster][movie] = 1
        else:
            clusters[cluster][movie] += 1
    
    # Transform raw movie counts to movie probabilities within cluster
    for cluster, movies in clusters.iteritems():
        for movie, count in movies.iteritems():
            clusters[cluster][movie] = float(count) / clusters_count[cluster]

    return clusters

def fit_and_get_lda(matrix):
    lda = dec.LatentDirichletAllocation(n_topics=n_topics, n_jobs=-1,
        learning_method='batch', verbose=3, max_iter=lda_max_iter)
    lda.fit(matrix)
    return lda

def get_account_topic_matrix(lda_transform, acc_by_index):
    acc_top_matr = {}
    for i, topics_dist in enumerate(lda_transform):
        acc_top_matr[acc_by_index[i]] = topics_dist
    return acc_top_matr

def get_topic_cluster_matrix(lda_components):
    top_clus_matr = []
    for t_clusters in normalize(lda_components, axis=1, norm='l1'):
        top_clus_matr.append(t_clusters)
    return top_clus_matr

if __name__ == '__main__':
    ##### Construct account - cluster matrix
    matr, accounts = get_cluster_matrix(sys.argv[1])
    lda = fit_lda(matr)

    transformed = lda.transform(matr)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    ##### Get accounts with 2 or more topics with "topic_p >= min_topic_p"
    micro_cands = {}
    for i, topics_dist in enumerate(transformed):
        good_nums = 0
        for num in topics_dist:
            if num >= min_topic_p:
                good_nums = good_nums + 1
        if good_nums > 1:
            micro_cands[acc_by_index[i]] = topics_dist
            #print good_nums

    print "Accounts: {}".format(len(accounts))
    print "Micro-profile cands.: {}".format(len(micro_cands))
    

    ##### Print each cluster's importance in a topic if "cluster_p >= min_topic_p"
    # components = normalize(lda.components_, axis=1, norm='l1')
    # for topic in components:
    #     clusters = []
    #     for i in xrange(len(topic)):
    #         cluster = topic[i]
    #         if cluster >= min_topic_p:
    #             clusters.append("{:>2}: {:>6.4f}".format(i, cluster))
    #     print clusters

    ##### Let's make a visualization
    # img = Image.new('RGB', (n_clusters, len(components)), '#FFFFFF')
    # for i in xrange(len(components)):
    #     for j in xrange(n_clusters):
    #         pixel = 255 - int(255 * components[i, j])
    #         img.putpixel((j, i), (pixel, pixel, pixel))

    # img.save('banana.png')


    ##### Test if lda output (transormed) and components_ can produce input matrix
    # for topic in transformed.dot(normalize(lda.components_, axis=1, norm='l1')):
        # print "{} {}".format(sum(topic), topic)

    ##### Print topics for each account with more than one topic where "topic_p >= min_topic_p"
    # for u_hash, topic_dist in micro_cands.iteritems():
    #     topics = []
    #     for i, p in enumerate(topic_dist):
    #         if p >= min_topic_p:
    #             topics.append("{:>2}: {:>6.4f}".format(i, p))
    #     print "{} {}".format(u_hash, topics)

    
