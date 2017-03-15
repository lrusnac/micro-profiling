import numpy as np
from tqdm import tqdm
from scipy.sparse import coo_matrix
from scipy.sparse import csc_matrix
import random
import math

class KMeans(object):
    def __init__(self, df, n_clusters):
        self.df = df.tocsc()  # np sparce matrix
        self.n_clusters = n_clusters
        self.centroids = None
        self.labels = np.ones(self.df.shape[1], dtype=int)

        self._precomputed_squared_points = np.zeroes(self.df.shape[1])
        self._precomputed_squared_centroids = np.zeroes(n_clusters)

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

        for i in tqdm(xrange(self.df.shape[1])):  # TODO: parallelize this
            point = self.df.getcol(i)

            min_distance = 100
            closest_centroid = -1

            # going through all centroids
            for j in xrange(self.centroids.shape[1]):
                centroid = self.centroids.getcol(j)

                dist = self.distance(point, centroid)
                if dist < min_distance:
                    closest_centroid = j
                    min_distance = dist

            if closest_centroid == -1:
                print 'something wrong happened in finding the closest_centroid'

            labels[i] = closest_centroid

        return labels

    def distance(self, p1, p2, i, j):
        ab = (p1.transpose()).dot(p2)[0,0]
        if ab == 0:
            return 1
        # aa = (p1.transpose()).dot(p1)[0,0]
        # bb = (p2.transpose()).dot(p2)[0,0]
        # return 1 - ab / (math.pow(aa, 0.5) * math.pow(bb, 0.5))

        aa = self._precomputed_squared_points(i)
        bb = self._precomputed_squared_centroids(j)

        return 1 - ab / (aa * bb)


    def _to_continue(self, old_centroids, new_centroids, iterations):
        return iterations < 50  # TODO make something smarter

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
        while self._to_continue(old_centroids, self.get_centroids(), iterations):
            print iterations
            iterations += 1

            old_centroids = self.centroids
            self.labels = self.get_labels()
            self.centroids = self.get_centroids()
