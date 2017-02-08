import zipfile
import csv
import os
import sys
import __main__

DEFAULT_NAME = '../00-common/10_percent_with_time_fields_clean_genres'

csv.field_size_limit(1000000000)

def get_zip_data_file_pointer(zipPath, csvName):
    zf = zipfile.ZipFile(zipPath)
    r = csv.DictReader(zf.open(csvName), delimiter=';')
    return r

def get_csv_data_file_pointer(csvPath):
    f = open(csvPath)
    r = csv.DictReader(f, delimiter=';')
    return r

def get_data_file_pointer(args):
    print '### STATS ###'
    currScript = os.path.realpath(__main__.__file__)
    currScript = currScript[currScript.index('micro-profiling') - len(currScript):]
    print 'Script: ' + currScript
    print 'Data: ' + (DEFAULT_NAME.split('/')[-1] if len(args) < 2 else args[1])
    print

    # Use default data file
    if len(args) < 2:
        zipPath = DEFAULT_NAME + '.zip'
        csvName = DEFAULT_NAME.split('/')[-1] + '.csv'
        return get_zip_data_file_pointer(zipPath, csvName)

    if args[1].endswith('.zip'):
        csvName = args[1].split('/')[-1][0:-4] + '.csv'
        return get_zip_data_file_pointer(args[1], csvName)
    if args[1].endswith('.csv'):
        return get_csv_data_file_pointer(args[1])