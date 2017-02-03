import zipfile
import csv
import os
from tqdm import tqdm

PATH = '../00-common/'
ZIPFILEPATH = 'no_serier_pruned_columns'
OUTFILEPATH = 'no_serier_pruned_columns_10_percent'

csv.field_size_limit(1000000000)
frequencies = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        if entry['hashed_ID'] not in frequencies:
            frequencies[entry['hashed_ID']] = 0
        frequencies[entry['hashed_ID']] = frequencies[entry['hashed_ID']] + 1

    customers_80_90 = sorted(frequencies, key=frequencies.get, reverse=True)[70000:140000]
    customers_80_90 = frozenset(customers_80_90)
    fields = [ 'hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID' ]

    with open(OUTFILEPATH + '.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer()

        for entry in tqdm(csvfile, total=16100000):
            if entry['hashed_ID'] in customers_80_90:
                writer.writerow(map(lambda field: entry[field], fields))
