import zipfile
import csv
import math
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from tqdm import tqdm

counters = {}
frequencies = {}

if __name__ == '__main__':
    rows_count = 0
    trainset = get_data_file_pointer(sys.argv[1])
    # count number of times movies appear
    for entry in tqdm(trainset, total=1771550):
        rows_count = rows_count + 1
        if entry['VM_TITLE'] not in counters:
            counters[entry['VM_TITLE']] = 0
        counters[entry['VM_TITLE']] = counters[entry['VM_TITLE']] + 1

    # calculate movies' frequencies
    for movie in sorted(counters, key=counters.get, reverse=True):
        f = counters[movie]/float(rows_count)
        frequencies[movie] = f

    testset = get_data_file_pointer(sys.argv[2])
    entry_count = 0
    guess_accuracy_sum = 0
    for entry in tqdm(testset, total=805243):
        movie = entry['VM_TITLE']
        if movie in frequencies:
            guess_accuracy_sum = guess_accuracy_sum + frequencies[movie]
        entry_count = entry_count + 1

    print guess_accuracy_sum / entry_count
