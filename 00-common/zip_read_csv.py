#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import csv

ZIPFILEPATH = 'YouseePlay_stream_data.zip'
CSVFILEPATH = 'YouseePlay_stream_data.csv'

csv.field_size_limit(1000000000)

def get_data_file_pointer():
    with zipfile.ZipFile(ZIPFILEPATH) as zf:
        r = csv.DictReader(zf.open(CSVFILEPATH), delimiter=';')
        return r


if __name__ == '__main__':
     csvfile = get_data_file_pointer()
     print csvfile.next()

