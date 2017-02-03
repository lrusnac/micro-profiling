import zipfile
import csv
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PATH = '../00-common/'
ZIPFILEPATH = 'data_pruned_columns_series'

csv.field_size_limit(1000000000)
frequencies = {}
counters = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open('YouseePlay_stream_data.csv'), delimiter=';')
        return r

def addEntryGenre(user, genre):
    if user not in frequencies:
        frequencies[user] = {}

    if genre not in frequencies[user]:
        frequencies[user][genre] = 0

    frequencies[user][genre] = frequencies[user][genre] + 1

if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        user = entry['hashed_ID']
        genres = entry['VM_GENRE'].split(',')
        if genres[0] == '':
            addEntryGenre(user, 'Unknown')
        else:
            for genre in genres:
                addEntryGenre(user, genre)

        # Increment once for each entry
        if user not in counters:
            counters[user] = 0
        counters[user] = counters[user] + 1

    for user, genres in frequencies.iteritems():
        for g in sorted(genres, key=genres.get, reverse=True):
            f = genres[g]/float(counters[user])
            frequencies[user][g] = f

    print counters
