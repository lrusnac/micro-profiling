import zipfile
import csv
import sys
from common import get_data_file_pointer
from tqdm import tqdm

from datetime import datetime

OUTFILEPATH = '10_percent_with_time_fields'

if __name__ == '__main__':
    fields = ['hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID', 'HOUR_OF_DAY', 'DAY_OF_WEEK']

    with open(OUTFILEPATH + '.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer(sys.argv)

        for entry in tqdm(csvfile, total=2576791):
            date = entry['STREAM_START_DATE']
            date = datetime.strptime(date, '%d%b%Y:%H:%M:%S.%f')
            # date = dateutil.parser.parse(entry['STREAM_START_DATE'])

            hour_of_day = date.hour
            entry['HOUR_OF_DAY'] = hour_of_day

            day_of_week = date.weekday()
            entry['DAY_OF_WEEK'] = day_of_week

            writer.writerow(map(lambda field: entry[field], fields))
