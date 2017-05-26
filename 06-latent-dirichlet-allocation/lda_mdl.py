import sys
import math
sys.path.insert(0, '../00-common')

from common import get_data_file_pointer
from common import get_line_count

from lda import *

from tqdm import tqdm
import numpy

LDA_MAX_ITER = 20
N_TOPICS = 40

lda = None
doc_topic_matr = None
top_term_matr = None
train_matr = None
train_transform = None
accounts = None
movie_by_index = None

def build_lda_model(train_file):
    global accounts
    global train_matr
    global movie_by_index
    global lda
    train_matr, accounts, movie_by_index = get_user_movie_matrix(train_file)

    # remove duplicates
    train_matr.sum_duplicates()
    train_matr.data = numpy.ones(len(train_matr.col))

    lda = fit_and_get_lda(train_matr, N_TOPICS, LDA_MAX_ITER)

if __name__ == '__main__':
    data_file = sys.argv[1]
    build_lda_model(data_file)

    # Transform account-cluster matrix according to fitted LDA
    train_transform = lda.transform(train_matr)

    acc_by_index = [''] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Get account-topic matrix from transformed matrix
    doc_topic_matr = get_account_topic_matrix(train_transform, acc_by_index)

    # for account, topics in doc_topic_matr.iteritems():
    #     print '{};{}'.format(account, ';'.join(str(t) for t in topics))
    # print

    # Get topic-cluster matrix from LDA components
    top_term_matr = get_topic_term_matrix(lda.components_, movie_by_index)

    # print 'TOPIC;{}'.format(';'.join(top_term_matr[0].iterkeys()))
    # for topic, movie_dict in top_term_matr.iteritems():
    #     p_vals = [str(p) for p in movie_dict.itervalues()]
    #     print '{};{}'.format(topic, ';'.join(p_vals))

    # Filter small values
    for account, topics in doc_topic_matr.iteritems():
        filtered = 0
        unfiltered_sum = 0
        for i, p in enumerate(topics):
            if p < 0.01:
                topics[i] = 0
                filtered += 1
            else:
                unfiltered_sum += p
        for i, p in enumerate(topics):
            if p == 0:
                topics[i] = (1 - unfiltered_sum) / filtered
        

    for topic, movie_dict in top_term_matr.iteritems():
        filtered = 0
        unfiltered_sum = 0
        for movie in movie_dict:
            if movie_dict[movie] < 0.1:
                movie_dict[movie] = 0
                filtered += 1
            else:
                unfiltered_sum += movie_dict[movie]
        for movie in movie_dict:
            if movie_dict[movie] == 0:
                movie_dict[movie] = (1 - unfiltered_sum) / filtered

    # calculate entropy
    dataset = get_data_file_pointer(data_file)
    guess_accuracy_sum = 0
    entries = 0
    for entry in tqdm(dataset, total=get_line_count(data_file)):
        user = entry['hashed_ID']
        movie = entry['VM_TITLE']
        entries += 1

        if user in doc_topic_matr and\
            movie in top_term_matr[0]: # Redundant check
            p = sum(t_p * top_term_matr[i][movie]
                for i, t_p in enumerate(doc_topic_matr[user]))
            guess_accuracy_sum -= math.log(p, 2)

    print 'Entropy: {}'.format(guess_accuracy_sum / entries)
    