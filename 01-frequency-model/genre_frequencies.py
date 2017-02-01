import zipfile
import csv
import os

PATH = '../00-common/'
ZIPFILEPATH = 'no_serier_pruned_columns'

csv.field_size_limit(1000000000)
frequencies = {}


def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    rows_count = 0
    invalid_count = 0
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        # 'VM_GENRE'
        rows_count = rows_count + 1
        if entry['VM_GENRE'] is '':
            invalid_count = invalid_count + 1

    print "total rows: " + str(rows_count)
    print "rows without genre: " + str(invalid_count)
