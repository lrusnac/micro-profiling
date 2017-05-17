import numpy as np
from tqdm import tqdm
from scipy.sparse import coo_matrix
from scipy.sparse import csc_matrix
import random
import math

from joblib import Parallel, delayed
import multiprocessing

class KMeans(object):
    def __init__(self, df, n_clusters):
        self.df = df.tocsc()  # np sparce matrix
        self.n_clusters = n_clusters
        self.centroids = None
        self.labels = np.ones(self.df.shape[1], dtype=int)

        self._precomputed_squared_points = np.zeros(self.df.shape[1])
        self._precomputed_squared_centroids = np.zeros(n_clusters)

        self.num_cores = multiprocessing.cpu_count()

    def get_centroids(self):
        A = coo_matrix((np.ones(self.labels.size), (np.array(range(0, self.labels.size)), self.labels)), shape=(self.labels.size, self.n_clusters), dtype=np.int8).tocsc()

        new_centroids = self.df.dot(A)
        counts = np.squeeze(np.asarray(new_centroids.sum(0)))

        empty_clusters = np.where(counts == 0)[0]
        for empty_cluster in empty_clusters:
            counts[empty_cluster] = 1

        new_centroids = new_centroids / counts

        for empty_cluster in empty_clusters:
            new_centroids[:, empty_cluster] = self.df.getcol(random.randint(0, self.df.shape[1]-1)).todense()

        return csc_matrix(new_centroids)

    def get_labels(self):
        labels = np.ones(self.df.shape[1], dtype=int)

        # precompute points squared values
        for i in xrange(self.centroids.shape[1]):
            centroid = self.centroids.getcol(i)
            self._precomputed_squared_centroids[i] = math.sqrt(centroid.transpose().dot(centroid)[0,0])

        # for i in tqdm(xrange(self.df.shape[1])):  # TODO: parallelize this
        #     labels[i] = findClosestCentroid(i, self.df.getcol(i), self.centroids, self.distance)

        labels = Parallel(n_jobs=self.num_cores)(delayed(self.findClosestCentroid)(i, self.df.getcol(i), self.centroids) for i in tqdm(xrange(self.df.shape[1])))

        return labels

    def findClosestCentroid(i, point, centroids):
        min_distance = 100
        closest_centroid = -1

        # going through all centroids
        for j in xrange(centroids.shape[1]):
            centroid = centroids.getcol(j)

            # dist = distance(point, centroid, i, j)

            ab = (point.transpose()).dot(centroid)[0,0]
            dist = -1
            if ab == 0:
                dist = 1
            else:
                aa = self._precomputed_squared_points[i]
                bb = self._precomputed_squared_centroids[j]

                dist = 1 - ab / (aa * bb)

            if dist < min_distance:
                closest_centroid = j
                min_distance = dist

        if closest_centroid == -1:
            print 'something wrong happened in finding the closest_centroid'

        return closest_centroid

    def distance(self, p1, p2, i, j):
        ab = (p1.transpose()).dot(p2)[0,0]
        if ab == 0:
            return 1
        # aa = (p1.transpose()).dot(p1)[0,0]
        # bb = (p2.transpose()).dot(p2)[0,0]
        # return 1 - ab / (math.pow(aa, 0.5) * math.pow(bb, 0.5))

        aa = self._precomputed_squared_points[i]
        bb = self._precomputed_squared_centroids[j]

        return 1 - ab / (aa * bb)


    def _to_continue(self, labels, iterations):
        count = 0
        for i in xrange(len(labels)):
            if self.labels[i] != labels[i]:
                count += 1

        # print "{} points out of {} changed labels".format(count, len(labels))
        return count > 0 and iterations < 50

    # clustering columns, a column is a movie
    def fit(self):
        random.seed(42)
        # get n_clusters initial centroids
        indeces = [random.randint(0, self.df.shape[1]-1) for i in xrange(self.n_clusters)] # TODO duplicates
        self.centroids = self.df[:,indeces]

        # precompute points squared values
        for i in tqdm(xrange(self.df.shape[1])):
            point = self.df.getcol(i)
            self._precomputed_squared_points[i] = math.sqrt(point.transpose().dot(point)[0,0])

        iterations = 0
        old_centroids = None
        old_labels = np.zeros(self.df.shape[1], dtype=int)
        while self._to_continue(old_labels, iterations):
            # print 'starting iteration: {}'.format(iterations+1)
            iterations += 1

            old_centroids = self.centroids
            old_labels = self.labels
            self.labels = self.get_labels()
            self.centroids = self.get_centroids()
