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
import os
import cPickle
import md5

n_clusters = -1
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
    return (matr, accounts, range(0, n_clusters))

def get_genre_matrix(filepath):
    csvfile = get_data_file_pointer(filepath)

    ##### Remember index of each account (i.e. which order they appear in the transactions)
    # print 'Creating the hashmaps for accounts indexes'
    accounts = {}
    global n_clusters
    genre_set = set()
    for transact in tqdm(csvfile, total=get_line_count(filepath)):
        if transact['hashed_ID'] not in accounts:
            accounts[transact['hashed_ID']] = len(accounts)

        genre_set.add(transact['VM_GENRE'])

    n_clusters = len(genre_set)
    #print 'n_clusters ' + str(n_clusters)

    genre_by_index = [genre for genre in genre_set]
    genre_indices = dict((genre, i) for i, genre in enumerate(genre_set))

    col = []
    row = []

    csvfile = get_data_file_pointer(filepath)

    ##### Populate matrix: each transaction adds one to (hashed_ID, VM_GENRE)
    #print 'creating the rows and cols lists'
    for transact in tqdm(csvfile, total=get_line_count(filepath)):
        row.append(accounts[transact['hashed_ID']])
        col.append(genre_indices[transact['VM_GENRE']])

    ##### Sparse matrix
    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(len(accounts), n_clusters))
    return (matr, accounts, genre_by_index)

def get_user_movie_matrix(filepath):
    # create the sparse matrix
    n_trans = get_line_count(filepath)
    csvfile = get_data_file_pointer(filepath)
    movies = {}
    accounts = {}

    # Create the hashmaps for movies and accounts indices
    for transact in tqdm(csvfile, total=n_trans):
        if transact['VM_TITLE'] not in movies:
            movies[transact['VM_TITLE']] = len(movies)

        if transact['hashed_ID'] not in accounts:
            accounts[transact['hashed_ID']] = len(accounts)
    col = []
    row = []

    csvfile = get_data_file_pointer(filepath)

    # Create the rows and cols lists
    for transact in tqdm(csvfile, total=n_trans):
        col.append(movies[transact['VM_TITLE']])
        row.append(accounts[transact['hashed_ID']])

    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))),
        shape=(len(accounts), len(movies))) # should be a new sparse matrix

    movie_by_index = [movie for movie in sorted(movies, key=movies.get)]
    return matr, accounts, movie_by_index

def get_term_movie_matrix(filepath, term_key):
    csvfile = get_data_file_pointer(filepath)
    terms = {}
    terms_count = {}

    for trans in tqdm(csvfile, total=get_line_count(filepath)):
        term = trans[term_key]
        movie = trans['VM_TITLE']

        # Initialize/add movie list and count for cluster
        if term not in terms:
            terms[term] = {}
            terms_count[term] = 1
        else:
            terms_count[term] += 1

        # Initialize/add movie's count in cluster
        if movie not in terms[term]:
            terms[term][movie] = 1
        else:
            terms[term][movie] += 1

    # Transform raw movie counts to movie probabilities within cluster
    for term, movies in terms.iteritems():
        for movie, count in movies.iteritems():
            terms[term][movie] = float(count) / terms_count[term]

    return terms

def fit_and_get_lda(matrix, n_topics, max_iter):
    file_data = '{}{}{}{}{}'.format(matrix.row.tolist(), matrix.col.tolist(), matrix.data.tolist(), n_topics, max_iter)

    filename = md5.new(file_data).hexdigest()

    if os.path.isfile(filename):
        # print 'load lda from file'
        with open(filename, 'rb') as hf:
            lda = cPickle.load(hf)

        return lda
    else:
        # print 'fit and save lda to file'
        lda = dec.LatentDirichletAllocation(n_topics=n_topics, n_jobs=-1,learning_method='batch', verbose=3, max_iter=max_iter)
        lda.fit(matrix)

        with open(filename, 'wb') as hf:
            cPickle.dump(lda, hf)
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

def get_topic_term_matrix(lda_components, term_by_index):
    norm_components = normalize(lda_components, axis=1, norm='l1')
    top_term_matr = {}
    for i, terms_dist in enumerate(norm_components):
        top_term_matr[i] = dict((term, p) for term, p in zip(term_by_index, terms_dist))
    return top_term_matr

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
