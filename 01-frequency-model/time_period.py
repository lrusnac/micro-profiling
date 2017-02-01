import zipfile
import csv
from datetime import datetime

PATH = '../00-common/'
ZIPFILEPATH = 'YouseePlay_stream_data'

csv.field_size_limit(1000000000)
min_date = datetime.max
max_date = datetime.min

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    for entry in csvfile:
        time = entry['STREAM_START_DATE']
        time = datetime.strptime(time, '%d%b%Y:%H:%M:%S.%f')

        if time < min_date:
            min_date = time

        if time > max_date:
            max_date = time

    print 'from: ' + str(min_date) + ' to: ' + str(max_date)
    # from: 2016-01-01 00:00:14 to: 2016-12-20 23:59:38.957000
