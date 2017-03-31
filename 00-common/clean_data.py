import sys
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta
import csv
import math

from common import get_data_file_pointer
from common import get_line_count

def clean_duplicates(entries):
    # Group by movie titles
    movies = set(map(lambda e: e['VM_TITLE'], entries))
    entry_groups = [[e for e in entries if e['VM_TITLE']==m] for m in movies]
    out_entries = []

    for group in entry_groups:
        # Remove "non-movies"
        if group[0]['VM_TITLE'] in ['HBO Nordic', 'YouSee Film & Serier', 'C More']:
            break
        s_group = sorted(group, key=lambda e: e['DATE_OBJ'])
        last_date = datetime.min

        for entry in s_group:
            diff = (entry['DATE_OBJ'] - last_date).total_seconds() / 60
            if diff > max(int(entry['VM_RUN_TIME']) * 2, 120):
                out_entries.append(entry)
                last_date = entry['DATE_OBJ']

    return out_entries


def clean_and_write_entries(writer, entries, fields):
    for e in clean_duplicates(user_hist):
        writer.writerow(map(lambda field: e[field], fields))

if __name__ == '__main__':
    filepath = sys.argv[1]
    out_filepath = '.'.join(filepath.split('/')[-1].split('.')[:-1]) + '_clean.csv'
    fields = [
        'TRANS_ID',
        'hashed_ID',
        'VM_TITLE',
        'VM_PRODUCTION_YEAR',
        'VM_GENRE',
        'VM_RUN_TIME',
        'STREAM_START_DATE',
        'VOD_CONTENT_TYPE',
        'VM_IMDBID',
        'HOUR_OF_DAY',
        'DAY_OF_WEEK']
    user_hash = ''
    user_hist = []

    with open(out_filepath, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer(filepath)
        
        for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
            # Remove series
            if 'Serier' in entry['VOD_CONTENT_TYPE']:
                continue
            
            # Add simplified timestamps
            date = entry['STREAM_START_DATE']
            date = datetime.strptime(date, '%d%b%Y:%H:%M:%S.%f')
            entry['HOUR_OF_DAY'] = date.hour
            entry['DAY_OF_WEEK'] = date.weekday()
            entry['DATE_OBJ'] = date

            # Clean genres (group adult genres)
            genres = entry['VM_GENRE']
            if 'Erotik' in genres or 'European' in genres or\
                'Amateur' in genres or 'Nordic' in genres:
                entry['VM_GENRE'] = 'adult'
            else:
                genres = genres.lower().split(',')
                if genres[0] == '':
                    entry['VM_GENRE'] = 'unknown'
                else:
                    entry['VM_GENRE'] = ','.join(sorted(genres))

            if entry['hashed_ID'] != user_hash:
                clean_and_write_entries(writer, user_hist, fields)
                user_hist = []
                user_hash = entry['hashed_ID']

            user_hist.append(entry)

        # Write out the last user's history
        clean_and_write_entries(writer, user_hist, fields)

            