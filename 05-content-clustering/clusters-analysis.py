import sys
import numpy as np
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer

import csv
from tqdm import tqdm
from scipy.sparse import coo_matrix

from PIL import Image

accounts = {}
n_clusters = -1

if __name__ == "__main__":
    # create the sparse matrix
    csvfile = get_data_file_pointer(sys.argv[1])

    print 'Creating the hashmaps for accounts indexes'
    for transact in tqdm(csvfile, total=2576791):
        if transact['hashed_ID'] not in accounts:
	    accounts[transact['hashed_ID']] = len(accounts)

        if int(transact['KMeans']) > n_clusters:
            n_clusters = int(transact['KMeans'])

    n_clusters += 1
    print 'n_clusters ' + str(n_clusters)

    col = []
    row = []

    csvfile = get_data_file_pointer(sys.argv[1])

    print 'creating the rows and cols lists'
    for transact in tqdm(csvfile, total=2576791):
        row.append(accounts[transact['hashed_ID']])
        col.append(int(transact['KMeans']))

    matr = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(len(accounts), n_clusters))

    matr = matr.tocsr()

    img = Image.new('RGB', (n_clusters, len(accounts)), '#FFFFFF')
    for i in xrange(len(accounts)):
        maxrow = matr.getrow(i).max()
        for j in xrange(n_clusters):
            pixel = 255
            if matr[i, j] != 0:
                pixel = 200 - int(200/maxrow * matr[i, j])

            img.putpixel((j, i), (pixel, pixel, pixel))
            
    img.save('image.png')
