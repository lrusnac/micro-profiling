import sys
import numpy as np
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer

import csv
from tqdm import tqdm
from scipy.sparse import coo_matrix

from KMeans import KMeans

OUTFILEPATH = 'clustered.csv'

movies = {}
accounts = {}

if __name__ == '__main__':
    # create the sparse matrix
    csvfile = get_data_file_pointer(sys.argv[1])

    print 'Creating the hashmaps for movies and accounts indexes'
    for transact in tqdm(csvfile, total=805242):
        if transact['VM_TITLE'] not in movies:
            movies[transact['VM_TITLE']] = len(movies)

        if transact['hashed_ID'] not in accounts:
	    accounts[transact['hashed_ID']] = len(accounts)
    col = []
    row = []

    csvfile = get_data_file_pointer(sys.argv[1])

    print 'creating the rows and cols lists'
    for transact in tqdm(csvfile, total=805242):
        col.append(movies[transact['VM_TITLE']])
        row.append(accounts[transact['hashed_ID']])

    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(len(accounts), len(movies))) # should be a new sparse matrix
    # add 1 to the movie,account coordinates
    matr.sum_duplicates()
    matr.data = np.ones(len(matr.col))
    print matr.shape

    print 'number of movies: ' + str(len(movies))
    print 'number of accounts: ' + str(len(accounts))

    # print dataset
    kmeans = KMeans(matr, 10).fit()
    labels =  kmeans.labels
    print labels

    # merge dataset with labels and do the cross validation as we do with genres
    # save new col as 'KMeans'

    # fields = ['hashed_ID', 'VM_TITLE', 'VM_PRODUCTION_YEAR', 'VM_GENRE', 'VM_RUN_TIME', 'VM_RATING', 'STREAM_START_DATE', 'VOD_CATEGORY', 'VOD_CONTENT_TYPE', 'VM_IMDBID', 'HOUR_OF_DAY', 'DAY_OF_WEEK', 'KMeans']
    #
    # with open(OUTFILEPATH, 'w') as output:
    #     writer = csv.writer(output, delimiter=';')
    #     writer.writerow(fields)
    #     csvfile = get_data_file_pointer(sys.argv[1])
    #
    #     for entry in tqdm(csvfile, total=1771549):
    #         entry['KMeans'] = labels[movies[entry['VM_TITLE']]]
    #
    #         writer.writerow(map(lambda field: entry[field], fields))
