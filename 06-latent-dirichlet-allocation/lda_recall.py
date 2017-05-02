import sys
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

def compute_recall(account, k=20):
    # accounts ==== all the transactions of one user, must not be empty
    customer = account[0]['hashed_ID']
    relevant_docs = set(map(lambda x: x['VM_TITLE'], account))

    # select the row for customer
    # compute the probability of each movie to be predicted
    #       and get the top k that the user didn't see yet

    predictions = train_transform[accounts[customer]].dot(lda.components_)
    selected_k = np.argpartition(predictions, -k)[-k:]

    k_movie_set = set([movie_by_index[i] for i in selected_k])
    # make k predictions for each account
    #   |relevant docs intersect retrieved docs| / |relevant docs|

    return len(relevant_docs & k_movie_set) / float(len(relevant_docs))

def metric_agregator(account):
    return (compute_recall(account, 10), compute_recall(account, 20), compute_recall(account, 50))

def metrics_evaluater(filepath, metrics):
    account = []
    previous_customer = ''

    result_list = []

    csvfile = get_data_file_pointer(filepath)
    for entry in tqdm(csvfile, total=get_line_count(filepath)):
        if previous_customer is not '' and entry['hashed_ID'] == previous_customer:
            account.append(entry)
        else:
            # new customer
            if previous_customer is not '':
                result_list.append(metrics(account))
            previous_customer = entry['hashed_ID']
            account = []
            account.append(entry)
    result_list.append(metrics(account))
    return result_list

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
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    build_lda_model(train_file)

    # Transform account-cluster matrix according to fitted LDA
    train_transform = lda.transform(train_matr)

    acc_by_index = [''] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Get account-topic matrix from transformed matrix
    doc_topic_matr = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_term_matr = get_topic_term_matrix(lda.components_, movie_by_index)

    results = metrics_evaluater(test_file, metric_agregator)
    print [sum(y) / len(y) for y in zip(*results)]

