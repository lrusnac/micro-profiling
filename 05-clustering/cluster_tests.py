import sys
import numpy as np
import sklearn.cluster as cl
import csv
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from tqdm import tqdm

OUTFILEPATH = 'cluster'

if __name__ == '__main__':
    # dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 3, 10, 11), dtype=None, names=True, comments='@')
    dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 10, 11), dtype=None, skip_header=1, comments='@')

    print dataset

    kmeans = cl.KMeans(n_jobs=-1).fit(dataset)
    print kmeans
    print kmeans.labels_
    print kmeans.cluster_centers_

    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    print(labels)

    # merge dataset with labels and do the cross validation as we do with genres

    # save new col as 'KMeans'
    fields = ['hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID', 'HOUR_OF_DAY', 'DAY_OF_WEEK', 'KMeans']

    with open(OUTFILEPATH + '_train.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer(sys.argv[1])

        i = 0
        for entry in tqdm(csvfile, total=1771549):
            entry['KMeans'] = labels[i]
            i = i + 1

            writer.writerow(map(lambda field: entry[field], fields))

    with open(OUTFILEPATH + '_test.csv', 'w') as output:
        writer = csv.writer(output, delimiter=';')
        writer.writerow(fields)
        csvfile = get_data_file_pointer(sys.argv[2])

        for entry in tqdm(csvfile, total=805242):
            line = np.array([entry['VM_PRODUCTION_YEAR'], entry['HOUR_OF_DAY'], entry['DAY_OF_WEEK']])
            line.reshape(-1, 1)
            entry['KMeans'] = kmeans.predict(line)[0]

            writer.writerow(map(lambda field: entry[field], fields))
