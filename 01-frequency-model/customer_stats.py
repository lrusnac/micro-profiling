import zipfile
import csv
import os

PATH = '../00-common/'
ZIPFILEPATH = 'YouseePlay_stream_data'

csv.field_size_limit(1000000000)
frequencies = {}


def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    rows_count = 0
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        rows_count = rows_count + 1
        if entry['hashed_ID'] not in frequencies:
            frequencies[entry['hashed_ID']] = 0
        frequencies[entry['hashed_ID']] = frequencies[entry['hashed_ID']] + 1

    print 'total lines: ' + str(rows_count)
    print 'total unique customers: ' + str(len(frequencies))
    print '\n\n'

    for w in sorted(frequencies, key=frequencies.get, reverse=True):
          print w, frequencies[w]
