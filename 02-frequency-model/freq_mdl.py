import zipfile
import csv
import math
import sys
from itertools import *
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from tqdm import tqdm

counters = {}
frequencies = []
movie2index = {}
c = 11.5

if __name__ == '__main__':
    rows_count = 0
    dataset = get_data_file_pointer(sys.argv[1])
    # count number of times movies appear
    for entry in tqdm(dataset, total=get_line_count(sys.argv[1])):
        rows_count = rows_count + 1
        if entry['VM_TITLE'] not in counters:
            counters[entry['VM_TITLE']] = 0
        counters[entry['VM_TITLE']] = counters[entry['VM_TITLE']] + 1

    # calculate movies' frequencies
    for i, movie in enumerate(sorted(counters, key=counters.get, reverse=True)):
        p = counters[movie]/float(rows_count)
        p = round(c * math.log(1/p, 2), 0)
        p = math.pow(math.pow(2, p/c), -1)
        frequencies.append(p)
        movie2index[movie] = i
    
    freq2 = []
    sum_of_p = sum(frequencies)
    for f in frequencies:
        freq2.append(f + (1-sum_of_p) * (f / float(sum_of_p)))

    frequencies = freq2

    c_movies = len(frequencies)
    for i in xrange(0, int(c_movies / 100)):
        top_n = (i+1) * 100
        top_movies = takewhile(lambda x: x >= frequencies[top_n-1], frequencies)
        top_movies = [x for x in top_movies]
        def_val = float(1 - sum(top_movies)) / (c_movies - top_n)
        dataset = get_data_file_pointer(sys.argv[1])
        entry_count = 0
        guess_accuracy_sum = 0
        for entry in tqdm(dataset, total=get_line_count(sys.argv[1])):
            movie = entry['VM_TITLE']
            p = frequencies[movie2index[movie]]
            p = p if p >= frequencies[top_n-1] else def_val
            if p <= 0:
                print 'p: {}, top_n-1 {}, freq: {}, defval: {}'.format(p, top_n-1, frequencies[top_n-1], def_val)
            guess_accuracy_sum -= math.log(p, 2)
            entry_count += 1

        print '{};{}'.format(
            guess_accuracy_sum / float(entry_count),
            len(top_movies))
        sys.stdout.flush()
