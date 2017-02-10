import zipfile
import csv
from datetime import datetime
from tqdm import tqdm
import json
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer


csv.field_size_limit(1000000000)
genres_stats = {}

if __name__ == '__main__':
    csvfile = get_data_file_pointer(sys.argv[1])

    for entry in tqdm(csvfile, total=2576791):
        genres = entry['VM_GENRE'].split(',')

        for genre in genres:
            if genre not in genres_stats:
                genres_stats[genre] = [0 for i in range(24)]

            genres_stats[genre][int(entry['HOUR_OF_DAY'])] += 1

    for genre in genres_stats:
        # frequencies by genre
        genre_views = sum(genres_stats[genre])
        for j in range(24):
            genres_stats[genre][j] /= float(genre_views)

    print genres_stats
