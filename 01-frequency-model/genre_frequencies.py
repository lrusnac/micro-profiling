import zipfile
import csv
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PATH = '../00-common/'
ZIPFILEPATH = 'no_serier_pruned_columns'

csv.field_size_limit(1000000000)
frequencies = {}
counters = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r

def addEntryGenre(genre, movie):
    if genre not in frequencies:
        frequencies[genre] = {}

    if movie not in frequencies[genre]:
        frequencies[genre][movie] = 0

    frequencies[genre][movie] = frequencies[genre][movie] + 1

    if genre not in counters:
        counters[genre] = 0

    counters[genre] = counters[genre] + 1

if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        genres = entry['VM_GENRE'].split(',')
        if genres == '':
            addEntryGenre('Unknown', entry['VM_TITLE'])

        for genre in genres:
            addEntryGenre(genre, entry['VM_TITLE'])

    for genre, genre_values in frequencies.iteritems():
        for w in sorted(genre_values, key=genre_values.get, reverse=True):
            f = genre_values[w]/float(counters[genre])
            frequencies[genre][w] = f

    print counters
