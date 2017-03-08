import sys
import numpy as np
import sklearn.cluster as cl

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
