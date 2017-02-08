import zipfile
import csv
from tqdm import tqdm

from datetime import datetime

PATH = '../00-common/'
ZIPFILEPATH = '10_percent_with_time_fields'
OUTFILEPATH = '10_percent_with_time_fields_clean_genres'

csv.field_size_limit(1000000000)

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    fields = ['hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID', 'HOUR_OF_DAY', 'DAY_OF_WEEK']

    with open(OUTFILEPATH + '.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer()

        for entry in tqdm(csvfile, total=2576791):
            genres = entry['VM_GENRE']
            if 'Erotik' in genres or 'European' in genres or 'Amateur' in genres or 'Nordic' in genres:
                entry['VM_GENRE'] = 'adult'
            else:
                genres = genres.lower().split(',')
                if genres[0] == '':
                    entry['VM_GENRE'] = 'unknown'
                else:
                    entry['VM_GENRE'] = ','.join(sorted(genres))

            writer.writerow(map(lambda field: entry[field], fields))
