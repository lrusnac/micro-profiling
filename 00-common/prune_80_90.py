import zipfile
import csv
import os
import sys
from common import get_data_file_pointer
from common import get_line_count
from tqdm import tqdm

OUTFILEPATH = 'pruned_80_90_customers.csv'

frequencies = {}

if __name__ == '__main__':
    if isinstance(sys.argv[2], basestring):
        OUTFILEPATH = sys.argv[2]

    csvfile = get_data_file_pointer(sys.argv[1])

    print 'Calculating distribution of users...'
    for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
        if entry['hashed_ID'] not in frequencies:
            frequencies[entry['hashed_ID']] = 0
        frequencies[entry['hashed_ID']] = frequencies[entry['hashed_ID']] + 1
    
    customer_count = len(frequencies)

    customers_80_90 = sorted(frequencies, key=frequencies.get,
        reverse=True)[int(customer_count*0.1) : int(customer_count * 0.2)]
    print 'Most: {}  Least: {}'.format(customers_80_90[0], customers_80_90[-1])
    customers_80_90 = frozenset(customers_80_90)
    fields = [ 'hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID' ]

    with open(OUTFILEPATH, 'w') as output:
        writer = csv.writer(output, delimiter=';')
        csvfile = get_data_file_pointer(sys.argv[1])
        writer.writerow(csvfile.fieldnames)

        print 'Wrinting 80 to 90 percentile users to file...'
        for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
            if entry['hashed_ID'] in customers_80_90:
                writer.writerow(map(lambda field: entry[field], csvfile.fieldnames))
