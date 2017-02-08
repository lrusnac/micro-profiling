import os
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer

frequencies = {}
counters = {}

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
    csvfile = get_data_file_pointer(sys.argv)
    for entry in csvfile:
        genres = entry['VM_GENRE'].split(',')
        if genres[0] == '':
            addEntryGenre('Unknown', entry['VM_TITLE'])
        else:
            for genre in genres:
                addEntryGenre(genre, entry['VM_TITLE'])

    for genre, genre_values in frequencies.iteritems():
        for w in sorted(genre_values, key=genre_values.get, reverse=True):
            f = genre_values[w]/float(counters[genre])
            frequencies[genre][w] = f

    print counters
