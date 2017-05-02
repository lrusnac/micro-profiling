import sys
sys.path.insert(0, '../00-common')

from common import get_data_file_pointer
from common import get_line_count

from tqdm import tqdm
import numpy

frequencies = {}
ordered_movies = []

def compute_recall(account, k=20):
    # accounts ==== all the transactions of one user, must not be empty
    customer = account[0]['hashed_ID']
    relevant_docs = set(map(lambda x: x['VM_TITLE'], account))

    k_movie_set = set(ordered_movies[:k])
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

def build_model(train_file):
    global frequencies
    counters = {}
    rows_count = 0
    trainset = get_data_file_pointer(train_file)
    # count number of times movies appear
    for entry in tqdm(trainset, total=get_line_count(train_file)):
        rows_count = rows_count + 1
        if entry['VM_TITLE'] not in counters:
            counters[entry['VM_TITLE']] = 0
        counters[entry['VM_TITLE']] = counters[entry['VM_TITLE']] + 1

    # calculate movies' frequencies
    for movie in sorted(counters, key=counters.get, reverse=True):
        f = counters[movie]/float(rows_count)
        frequencies[movie] = f

    global ordered_movies
    ordered_movies, _ = zip(*sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

if __name__ == '__main__':
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    build_model(train_file)

    results = metrics_evaluater(test_file, metric_agregator)
    print [sum(y) / len(y) for y in zip(*results)]
