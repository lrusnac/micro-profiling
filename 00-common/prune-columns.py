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
    fields = [ 'hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID' ]

    with open('output.csv', 'wb') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        for entry in csvfile:
            writer.writerow(map(lambda field: entry[field], fields))
