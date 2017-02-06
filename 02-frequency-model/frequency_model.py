#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import csv
import math

PATH = '../00-common/'
ZIPFILEPATH = 'no_serier_pruned_columns_10_percent'

csv.field_size_limit(1000000000)

counters = {}
frequencies = {}
h = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    rows_count = 0
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        rows_count = rows_count + 1
        if entry['VM_TITLE'] not in counters:
            counters[entry['VM_TITLE']] = 0
        counters[entry['VM_TITLE']] = counters[entry['VM_TITLE']] + 1

    for w in sorted(counters, key=counters.get, reverse=True):
        f = counters[w]/float(rows_count)
        frequencies[w] = f
        h[w] = -f * math.log(f, 2)
        print w, f, h[w]

    print 'entropy: ' + str(sum(h.values()))
