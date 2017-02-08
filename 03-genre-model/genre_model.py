import zipfile
import csv
import os
import math
from tqdm import tqdm

PATH = '../00-common/'
ZIPFILEPATH = '10_percent_with_time_fields_clean_genres'

csv.field_size_limit(1000000000)
user_genre = {}
user_genre_ph_table = {}
internal_user_counters = {}

genre_movie = {}
genre_movie_ph_table = {}
internal_genre_counter = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH+'.csv'), delimiter=';')
        return r

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

if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in tqdm(csvfile, total=2576791):
        user = entry['hashed_ID']
        addEntryGenre(user, entry['VM_GENRE'])
        addEntryMovie(entry['VM_TITLE'], entry['VM_GENRE'])

    # compute the user_genre_ph_table
    for user, genres in user_genre.iteritems():
        for g in genres:
            f = genres[g]/float(internal_user_counters[user])
            user_genre_ph_table[user][g] = (f, -f * math.log(f, 2))
        # Print user's entropy: sum of h's for his genres
        # print user + ' ' + str(sum([v[1] for v in user_genre_ph_table[user].values()]))

    # compute the genre_movie_ph_table
    for genre, genre_values in genre_movie.iteritems():
        for w in genre_values:
            f = genre_values[w]/float(internal_genre_counter[genre])
            genre_movie_ph_table[genre][w] = (f, -f * math.log(f, 2))

    # not right combination of the 2 things
    entropy = 0
    csvfile = get_data_file_pointer()
    for entry in tqdm(csvfile, total=2576791):
        p = user_genre_ph_table[entry['hashed_ID']][entry['VM_GENRE']][0] * genre_movie_ph_table[entry['VM_GENRE']][entry['VM_TITLE']][0]
        entropy += -p * math.log(p, 2)

    print entropy
