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
clus_by_index = None
term_movie_matr = None

def compute_recall_precision(account, predictions, movie_by_index, k=20):
    relevant_docs = set(map(lambda x: x['VM_TITLE'], account))

    selected_k = np.argpartition(predictions, -k)[-k:]

    k_movie_set = set([movie_by_index[i] for i in selected_k])

    return (len(relevant_docs & k_movie_set) / float(len(relevant_docs)), len(relevant_docs & k_movie_set) / float(k))

def metric_agregator(account):
    customer = account[0]['hashed_ID']
    cluster_predictions = train_transform[accounts[customer]].dot(lda.components_)
    # this will give me only clusters so need to multiply with movies frequencies for each cluster and then get the top k

    # combine predictions with term_movie_matr
    movie_by_index = []
    predictions = []
    for cluster in clus_by_index:
        str_cluster = str(cluster)
        for movie in term_movie_matr[str_cluster]:
            movie_by_index.append(movie)
            predictions.append(term_movie_matr[str_cluster][movie] * cluster_predictions[cluster])

    rp10 = compute_recall_precision(account, predictions, movie_by_index, 10)
    rp20 = compute_recall_precision(account, predictions, movie_by_index, 20)
    rp50 = compute_recall_precision(account, predictions, movie_by_index, 50)
    return (rp10[0], rp20[0], rp50[0], rp10[1], rp20[1], rp50[1])

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
    global clus_by_index
    global lda
    train_matr, accounts, clus_by_index = get_cluster_matrix(train_file)

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
    top_term_matr = get_topic_term_matrix(lda.components_, clus_by_index)

    # get movie frequencies inside each group
    term_movie_matr = get_term_movie_matrix(train_file, term_key='KMeans')

    results = metrics_evaluater(test_file, metric_agregator)
    print [sum(y) / len(y) for y in zip(*results)]
