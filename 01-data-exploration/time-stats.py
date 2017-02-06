import zipfile
import csv
from datetime import datetime
from tqdm import tqdm

PATH = '../00-common/'
ZIPFILEPATH = '10_percent_with_time_fields'

csv.field_size_limit(1000000000)
days = {}

def get_data_file_pointer():
    with zipfile.ZipFile(PATH + ZIPFILEPATH + '.zip') as zf:
        r = csv.DictReader(zf.open(ZIPFILEPATH + '.csv'), delimiter=';')
        return r


if __name__ == '__main__':
    for i in range(7):
        days[str(i)] = {}
        for j in range(24):
            days[str(i)][str(j)] = 0

    csvfile = get_data_file_pointer()

    for entry in tqdm(csvfile, total=2576791):
        days[entry['DAY_OF_WEEK']][entry['HOUR_OF_DAY']] = days[entry['DAY_OF_WEEK']][entry['HOUR_OF_DAY']] + 1

    print days

    # {'20': 323216, '21': 279446, '22': 159713, '23': 88025, '1': 21988, '0': 29710, '3': 9157, '2': 12610, '5': 15679, '4': 10109, '7': 42647, '6': 27594, '9': 65360, '8': 55109, '11': 82487, '10': 75015, '13': 103162, '12': 93905, '15': 126447, '14': 114704, '17': 172888, '16': 142567, '19': 294087, '18': 231166}
    # {'1': 262546, '0': 295813, '3': 274859, '2': 259510, '5': 569395, '4': 405286, '6': 509382}
