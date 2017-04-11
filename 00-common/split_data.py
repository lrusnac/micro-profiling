import zipfile
import csv
from tqdm import tqdm
import random
import sys

from common import get_data_file_pointer

# OUTFILEPATH = '10_percent_v01'

csv.field_size_limit(1000000000)

dataset_division = 0.7 # persentage of data for training
previous_customer = ''


def devide_and_write(train_writer, test_writer, stack):
    if len(stack) != 0:
        random.shuffle(stack)
        division_point = int(len(stack)*dataset_division + 0.5)
        write_list_to_csv(train_writer, stack[:division_point])
        write_list_to_csv(test_writer, stack[division_point:])

def write_list_to_csv(writer, lines):
    for line in lines:
        writer.writerow(map(lambda field: line[field], fields))

if __name__ == '__main__':
    OUTFILEPATH = sys.argv[1].split('/')[-1].split('.')[0]
    csvfile = get_data_file_pointer(sys.argv[1])

    fields = csvfile.fieldnames # ['hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID', 'HOUR_OF_DAY', 'DAY_OF_WEEK']
    stack = []

    with open(OUTFILEPATH + '_test' + '.csv', 'w') as test:
        test_writer = csv.writer(test, delimiter=';')
        test_writer.writerow(fields)
        with open(OUTFILEPATH + '_train' + '.csv', 'w') as train:
            train_writer = csv.writer(train, delimiter=';')
            train_writer.writerow(fields)

            for entry in tqdm(csvfile, total=2576791):
                if previous_customer is not '' and entry['hashed_ID'] == previous_customer:
                    stack.append(entry)
                else:
                    # new customer, devide the transactions and write them to file
                    devide_and_write(train_writer, test_writer, stack)
                    previous_customer = entry['hashed_ID']
                    stack = []
                    stack.append(entry)

            devide_and_write(train_writer, test_writer, stack)
