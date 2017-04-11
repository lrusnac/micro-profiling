import sys
import numpy as np
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

import csv
import math
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

    clusters = {k:v/float(lines) for k,v in clusters.items()}

    # print clusters
    # print len(clusters)

    csvfile = get_data_file_pointer(sys.argv[2])
    accuracy = 0
    loss = 0
    test_lines = get_line_count(sys.argv[2])
    for entry in tqdm(csvfile, total=test_lines):
        if entry[field_name] in clusters:
            accuracy -= math.log(clusters[entry[field_name]])
        else:
            loss += 1

    print 'entropy: {}'.format(accuracy / float(test_lines-loss))
    print 'loss: {}'.format(loss)
