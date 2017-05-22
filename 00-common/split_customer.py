import zipfile
import csv
from tqdm import tqdm
import random
import sys

from common import get_data_file_pointer
from common import get_line_count
import argparse
# OUTFILEPATH = '10_percent_v01'

csv.field_size_limit(1000000000)
time_interval_splits = sorted([6, 12, 23])

def hourToGroup(hour):
    hour = int(hour)
    if len(time_interval_splits) == 1:
        return '0'

    interval = 0
    for split in time_interval_splits:
        if hour < split:
            return str(interval)
        interval += 1

    return '0'


if __name__ == '__main__':
    #  $dataset -t -n$j -s$i
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-n', '--intervals', type=int, default=2, help='number of time intervals')
    parser.add_argument('-s', '--starting', type=int, default=0, help='stariting point')

    args = parser.parse_args()

    time_interval_splits = sorted([(x*(24/args.intervals)+args.starting)%24 for x in range(args.intervals)])

    filepath = args.file
    out_filepath = '.'.join(filepath.split('/')[-1].split('.')[:-1]) + '_divided_by_time.csv'

    csvfile = get_data_file_pointer(filepath)

    with open(out_filepath, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(csvfile.fieldnames)

        for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
            entry['hashed_ID'] = entry['hashed_ID'] + '-' + hourToGroup(entry['HOUR_OF_DAY'])

            writer.writerow(map(lambda field: entry[field], csvfile.fieldnames))
