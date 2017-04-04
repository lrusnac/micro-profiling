import sys
import numpy as np
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

import csv
from tqdm import tqdm

field_name = 'KMeans'
clusters = {}


if __name__ == '__main__':
    csvfile = get_data_file_pointer(sys.argv[1])

    lines = get_line_count(sys.argv[1])
    for entry in tqdm(csvfile, total=lines):
        if entry[field_name] not in clusters:
            clusters[entry[field_name]] = 0
        clusters[entry[field_name]] += 1

    print {k:v/float(lines) for k,v in clusters.items()}
