import sys
sys.path.insert(0, '../00-common')

from common import get_data_file_pointer
from common import get_line_count

from tqdm import tqdm
import numpy

user_genre = {}
user_genre_ph_table = {}
internal_user_counters = {}

genre_movie = {}
genre_movie_ph_table = {}
internal_genre_counter = {}

def compute_recall(account, k=20):
    # accounts ==== all the transactions of one user, must not be empty
    customer = account[0]['hashed_ID']
    relevant_docs = set(map(lambda x: x['VM_TITLE'], account))

    genres = {}
    for transaction in account:
        if transaction['VM_GENRE'] not in genres:
            genres[transaction['VM_GENRE']] = 0
        genres[transaction['VM_GENRE']] += 1

    k_movie_set = set()
    for genre in genres:
        genre_k = int(round(genres[genre] / float(len(account)) * k))

        k_movie_set |= sorted(genre_movie_ph_table[genres[genre]], key=genre_movie_ph_table[genres[genre]].get, reverse=True)[:genre_k]

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

def addEntryGenre(user, genre):
    if user not in user_genre:
        user_genre[user] = {}
        user_genre_ph_table[user] = {}

    if genre not in user_genre[user]:
        user_genre[user][genre] = 0

    user_genre[user][genre] = user_genre[user][genre] + 1

    if user not in internal_user_counters:
        internal_user_counters[user] = 0
    internal_user_counters[user] = internal_user_counters[user] + 1

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
        addEntryGenre(user, entry['VM_GENRE'])
        addEntryMovie(entry['VM_TITLE'], entry['VM_GENRE'])

    # compute the user_genre_ph_table
    for user, genres in user_genre.iteritems():
        for g in genres:
            f = genres[g]/float(internal_user_counters[user])
            user_genre_ph_table[user][g] = f

    # compute the genre_movie_ph_table
    for genre, genre_values in genre_movie.iteritems():
        for w in genre_values:
            f = genre_values[w]/float(internal_genre_counter[genre])
            genre_movie_ph_table[genre][w] = f

if __name__ == '__main__':
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    build_model(train_file)

    results = metrics_evaluater(test_file, metric_agregator)
    print [sum(y) / len(y) for y in zip(*results)]
