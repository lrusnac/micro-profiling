import zipfile
import csv
import os
import datetime
import sys
import __main__

csv.field_size_limit(1000000000)

def get_zip_data_file_pointer(zipPath, csvName):
    zf = zipfile.ZipFile(zipPath)
    r = csv.DictReader(zf.open(csvName), delimiter=';')
    return r

def get_csv_data_file_pointer(csvPath):
    f = open(csvPath)
    r = csv.DictReader(f, delimiter=';')
    return r

def get_data_file_pointer(data_file, do_print = False):
    # Only supply a path string
    if not isinstance(data_file, basestring):
        raise ValueError("specified data_file not of type 'string'")
    if do_print:
        print_stats(data_file)

    if data_file.endswith('.zip'):
        csvName = data_file.split('/')[-1][0:-4] + '.csv'
        return get_zip_data_file_pointer(data_file, csvName)
    elif data_file.endswith('.csv'):
        return get_csv_data_file_pointer(data_file)
    else:
        return None

def print_stats(data_file_path):
    print '### STATS ###'
    print 'Date: ' + str(datetime.datetime.now())
    curr_script = os.path.realpath(__main__.__file__)
    curr_script = curr_script[curr_script.index('micro-profiling') - len(curr_script):]
    print 'Script: ' + curr_script
    print 'Data: ' + data_file_path
    print