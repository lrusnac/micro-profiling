import zipfile
import csv
import math
import sys
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from tqdm import tqdm

counters = {}
frequencies = {}

if __name__ == '__main__':
    rows_count = 0
    trainset = get_data_file_pointer(sys.argv[1])
    # count number of times movies appear
    for entry in tqdm(trainset, total=get_line_count(sys.argv[1])):
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
    loss_count = 0
    guess_accuracy_sum = 0
    for entry in tqdm(testset, total=get_line_count(sys.argv[2])):
        movie = entry['VM_TITLE']
        if movie in frequencies:
            guess_accuracy_sum = guess_accuracy_sum - math.log(frequencies[movie],2)
            entry_count = entry_count + 1
        else:
            loss_count += 1


    print 'entropy: {}'.format(guess_accuracy_sum / float(entry_count))
    print 'loss: {}'.format(loss_count / float(loss_count + entry_count))
    print 'loss_count: {}'.format(loss_count)
