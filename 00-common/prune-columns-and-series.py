import zipfile
import csv
import os
import sys
from common import get_data_file_pointer

OUTFILEPATH = 'no_serier_pruned_columns'

if __name__ == '__main__':
    csvfile = get_data_file_pointer(sys.argv)
    fields = [ 'hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID' ]

    with zipfile.ZipFile(OUTFILEPATH + '.zip', 'w') as zfo:
        with open(OUTFILEPATH + '.csv', 'w') as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(fields)
            for entry in csvfile:
                if 'Serier' not in entry['VOD_CONTENT_TYPE']:
                    writer.writerow(map(lambda field: entry[field], fields))

        zfo.write(OUTFILEPATH + '.csv')
        os.remove(OUTFILEPATH + '.csv') # remove the temp csv file
