import zipfile
import csv
from datetime import datetime
from tqdm import tqdm
import json
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer


csv.field_size_limit(1000000000)
hours = []

if __name__ == '__main__':
    for i in range(24):
        hours.append({})

    csvfile = get_data_file_pointer(sys.argv[1])

    for entry in tqdm(csvfile, total=2576791):
        genres = entry['VM_GENRE'].split(',')
        for genre in genres:
            if genre not in hours[int(entry['HOUR_OF_DAY'])]:
                hours[int(entry['HOUR_OF_DAY'])][genre] = 0
            hours[int(entry['HOUR_OF_DAY'])][genre] += 1

    for i in range(24):
        # frequencies by hour
        hour_views = sum(hours[i].values())
        for j in hours[i].keys():
            hours[i][j] /= float(hour_views)

    print hours
