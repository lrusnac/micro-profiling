import zipfile
import csv
import os
import math
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from tqdm import tqdm

max_predictions = 50

user_genre = {}
user_genre_ph_table = {}
internal_user_counters = {}

genre_movie = {}
genre_movie_ph_table = {}
internal_genre_counter = {}

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

def makeUserPredictions(user):
    predictions = {}
    for genre_set, p_i in user_genre_ph_table[user].iteritems:
        for movie, q_x in genre_movie_ph_table[genre_set].iteritems:
            # check if movie appears in several genre sets?
            predictions[movie] = p_i * q_x
    return sorted(predictions, key=predictions.get, reverse=True)[:max_predictions]

if __name__ == '__main__':
    trainset = get_data_file_pointer(sys.argv[1], True)
    for entry in tqdm(trainset, total=1771550):
        user = entry['hashed_ID']
        addEntryGenre(user, entry['VM_GENRE'])
        addEntryMovie(entry['VM_TITLE'], entry['VM_GENRE'])

    # compute the user_genre_ph_table
    for user, genres in user_genre.iteritems():
        for g in genres:
            f = genres[g]/float(internal_user_counters[user])
            user_genre_ph_table[user][g] = f
        # Print user's entropy: sum of h's for his genres
        # print user + ' ' + str(sum([v[1] for v in user_genre_ph_table[user].values()]))

    # compute the genre_movie_ph_table
    for genre, genre_values in genre_movie.iteritems():
        for w in genre_values:
            f = genre_values[w]/float(internal_genre_counter[genre])
            genre_movie_ph_table[genre][w] = f

        print genre + " " + str(sum([v[1] for v in genre_movie_ph_table[genre].values()]))

    # load test set
    testset = get_data_file_pointer(sys.argv[2])
    entry_count = 0
    guess_accuracy_sum = 0
    for entry in tqdm(testset, total=805243):
        user = entry['hashed_ID']
        genre_set = entry['VM_GENRE']
        movie = entry['VM_TITLE']

        if genre_set in user_genre_ph_table[user]:
            if genre_set in genre_movie_ph_table:
                if movie in genre_movie_ph_table[genre_set]:
                    # add p_i * q_x
                    guess_accuracy_sum = guess_accuracy_sum + \
                        - math.log(user_genre_ph_table[user][genre_set] * \
                        genre_movie_ph_table[genre_set][movie], 2)
        entry_count = entry_count + 1

    print guess_accuracy_sum / entry_count
