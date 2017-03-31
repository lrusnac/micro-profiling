import sys
import os
from tqdm import tqdm

sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

frequencies = {}

if __name__ == '__main__':
    rows_count = 0
    csvfile = get_data_file_pointer(sys.argv[1])
    for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
        rows_count = rows_count + 1
        if entry['hashed_ID'] not in frequencies:
            frequencies[entry['hashed_ID']] = 0
        frequencies[entry['hashed_ID']] = frequencies[entry['hashed_ID']] + 1

    print 'total lines: ' + str(rows_count)
    print 'total unique customers: ' + str(len(frequencies))
    print '\n\n'

    for w in sorted(frequencies, key=frequencies.get, reverse=True):
          print w, frequencies[w]
