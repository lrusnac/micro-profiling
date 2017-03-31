import zipfile
import csv
import os
import math
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from tqdm import tqdm

time_interval_splits = sorted([0, 5, 11, 16])
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

def hourToGroup(hour):
    hour = int(hour)

    # Need at least two splitting points to give
    # different intervals
    if len(time_interval_splits) == 1:
        return '0'

    interval = 0
    for split in time_interval_splits:
        if hour < split:
            return str(interval)
        interval += 1
    
    # Not smaller than any of the splits,
    # i.e. it's later than the last, thus group 0
    return '0'

def nextPartOfDay(part_of_day):
    return str((int(part_of_day) + 1) % 4)

if __name__ == '__main__':
    trainset = get_data_file_pointer(sys.argv[1], True)
    for entry in tqdm(trainset, total=get_line_count(sys.argv[1])):
        user = entry['hashed_ID']
        addEntryGenre(user + '_' + hourToGroup(entry['HOUR_OF_DAY']), entry['VM_GENRE'])
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

    # load test set
    testset = get_data_file_pointer(sys.argv[2])
    entry_count = 0
    guess_accuracy_sum = 0
    zero_probability_rec = 0
    for entry in tqdm(testset, total=get_line_count(sys.argv[2])):
        user = entry['hashed_ID']
        genre_set = entry['VM_GENRE']
        movie = entry['VM_TITLE']
        part_of_day = hourToGroup(entry['HOUR_OF_DAY'])

        if user + '_' + part_of_day not in user_genre_ph_table:
            part_of_day = nextPartOfDay(part_of_day)

        if user + '_' + part_of_day not in user_genre_ph_table:
            part_of_day = nextPartOfDay(part_of_day)

        if user + '_' + part_of_day not in user_genre_ph_table:
            part_of_day = nextPartOfDay(part_of_day)

        if user + '_' + part_of_day not in user_genre_ph_table:
            part_of_day = nextPartOfDay(part_of_day)

        if genre_set in user_genre_ph_table[user + '_' + part_of_day]:
            if genre_set in genre_movie_ph_table:
                if movie in genre_movie_ph_table[genre_set]:
                    # add p_i * q_x
                    guess_accuracy_sum += - math.log(user_genre_ph_table[(user + '_' + part_of_day)][genre_set] * \
                        genre_movie_ph_table[genre_set][movie], 2)

                    entry_count = entry_count + 1
        else:
            zero_probability_rec += 1

    print 'Entropy: {}'.format(guess_accuracy_sum / entry_count)
    print 'Loss: {}'.format(zero_probability_rec / float(entry_count))
