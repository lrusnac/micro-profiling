import zipfile
import csv
import os
import sys
from common import get_data_file_pointer
from tqdm import tqdm

OUTFILEPATH = 'no_serier_pruned_columns_10_percent'

frequencies = {}

if __name__ == '__main__':
    csvfile = get_data_file_pointer(sys.argv)

    print 'Calculating distribution of users...'
    for entry in tqdm(csvfile, total=16100000):
        if entry['hashed_ID'] not in frequencies:
            frequencies[entry['hashed_ID']] = 0
        frequencies[entry['hashed_ID']] = frequencies[entry['hashed_ID']] + 1

    customers_80_90 = sorted(frequencies, key=frequencies.get, reverse=True)[70000:140000]
    customers_80_90 = frozenset(customers_80_90)
    fields = [ 'hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID' ]

    with open(OUTFILEPATH + '.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer(sys.argv)

        print 'Wrinting 80 to 90 percentile users to file...'
        for entry in tqdm(csvfile, total=16100000):
            if entry['hashed_ID'] in customers_80_90:
                writer.writerow(map(lambda field: entry[field], fields))
