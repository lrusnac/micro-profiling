import sys
sys.path.insert(0, '../00-common')

from common import get_data_file_pointer
from common import get_line_count

from tqdm import tqdm
import numpy

counters = {}

genre_movie = {}
genre_movie_ph_table = {}
internal_genre_counter = {}

k_movie_set = set()

def compute_recall(account, k=20):
    # accounts ==== all the transactions of one user, must not be empty
    customer = account[0]['hashed_ID']
    relevant_docs = set(map(lambda x: x['VM_TITLE'], account))

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

def addEntryGenre(genre):
    if genre not in counters:
        counters[genre] = 0

    counters[genre] = counters[genre] + 1

def addEntryMovie(movie, genre):
    if genre not in genre_movie:
        genre_movie[genre] = {}
        genre_movie_ph_table[genre] = {}

    if movie not in genre_movie[genre]:
        genre_movie[genre][movie] = 0

    genre_movie[genre][movie] = genre_movie[genre][movie] + 1

    if genre not in internal_genre_counter:
        internal_genre_counter[genre] = 0

    internal_genre_counter[genre] = internal_genre_counter[genre] + 1

def build_model(train_file):
    trainset = get_data_file_pointer(train_file, True)
    for entry in tqdm(trainset, total=get_line_count(train_file)):
        user = entry['hashed_ID']
        addEntryGenre(entry['VM_GENRE'])
        addEntryMovie(entry['VM_TITLE'], entry['VM_GENRE'])

    # compute the genre distribution
    freq = {}
    total = sum(counters.values())
    for genre in counters.iteritems():
        freq[genre] = counters[genre]/float(total)

    # compute the genre_movie_ph_table
    for genre, genre_values in genre_movie.iteritems():
        for w in genre_values:
            f = genre_values[w]/float(internal_genre_counter[genre])
            genre_movie_ph_table[genre][w] = f

    global k_movie_set
    for genre in user_genre_ph_table[customer]:
        genre_k = int(round(freq[genre] * k))

        k_movie_set |= set(sorted(genre_movie_ph_table[genre], key=genre_movie_ph_table[genre].get, reverse=True)[:genre_k])


if __name__ == '__main__':
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    build_model(train_file)

    results = metrics_evaluater(test_file, metric_agregator)
    print [sum(y) / len(y) for y in zip(*results)]
