#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
from tqdm import tqdm

sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

counters = {}
frequencies = {}
h = {}

if __name__ == '__main__':
    rows_count = 0
    csvfile = get_data_file_pointer(sys.argv[1], do_print = True)

    for entry in tqdm(csvfile, total=get_line_count(sys.argv[1])):
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
