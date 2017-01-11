#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import csv

ZIPFILEPATH = '../00-common/YouseePlay_stream_data.zip'
CSVFILEPATH = 'YouseePlay_stream_data.csv'

csv.field_size_limit(1000000000)

frequencies = {}

def get_data_file_pointer():
    with zipfile.ZipFile(ZIPFILEPATH) as zf:
        r = csv.DictReader(zf.open(CSVFILEPATH), delimiter=';')
        return r


if __name__ == '__main__':
    rows_count = 0
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        rows_count = rows_count + 1
        if entry['VM_TITLE'] not in frequencies:
            frequencies[entry['VM_TITLE']] = 0
        frequencies[entry['VM_TITLE']] = frequencies[entry['VM_TITLE']] + 1
    
    for w in sorted(frequencies, key=frequencies.get, reverse=True):
          print w, frequencies[w]/float(rows_count)
