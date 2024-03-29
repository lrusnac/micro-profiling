import zipfile
import csv
import os
import math

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PATH = '../00-common/'
ZIPFILEPATH = '10_percent_with_time_fields_clean_genres'

csv.field_size_limit(1000000000)
frequencies = {}
ph_table = {}
counters = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH+'.csv'), delimiter=';')
        return r

def addEntryGenre(user, genre):
    if user not in frequencies:
        frequencies[user] = {}
        ph_table[user] = {}

    if genre not in frequencies[user]:
        frequencies[user][genre] = 0

    frequencies[user][genre] = frequencies[user][genre] + 1

if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        user = entry['hashed_ID']
        genres = entry['VM_GENRE']
        if genres == '':
            addEntryGenre(user, 'Unknown')
        else:
            addEntryGenre(user, genres)

        # Increment once for each entry
        if user not in counters:
            counters[user] = 0
        counters[user] = counters[user] + 1

    for user, genres in frequencies.iteritems():
        for g in sorted(genres, key=genres.get, reverse=True):
            f = genres[g]/float(counters[user])
            ph_table[user][g] = (f, -f * math.log(f, 2))
        # Print user's sum of entropies for his genres
        print user + ' ' + str(sum([v[1] for v in ph_table[user].values()]))
