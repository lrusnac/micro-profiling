import zipfile
import csv

ZIPFILEPATH = 'data_pruned_columns.zip'
CSVFILEPATH = 'YouseePlay_stream_data.csv'

csv.field_size_limit(1000000000)

def get_data_file_pointer():
    with zipfile.ZipFile(ZIPFILEPATH) as zf:
        r = csv.DictReader(zf.open(CSVFILEPATH), delimiter=';')
        return r


if __name__ == '__main__':
    csvfile = get_data_file_pointer()
    fields = csvfile.fieldnames

    with open('data_pruned_series.csv', 'wb') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        for entry in csvfile:
            if entry['VOD_CONTENT_TYPE'] != 'Serier':
                writer.writerow(map(lambda field: entry[field], fields))
