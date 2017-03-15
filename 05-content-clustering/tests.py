import numpy as np
from scipy.sparse import coo_matrix

col = [1,2,0,1,2,0,1,2]
row = [0,0,1,1,1,2,2,3]
data = [1,1,1,1,1,1,1,1]

S = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(4, 3)).tocsc()
print S.todense()


col = [0,1,0]
row = [0,1,2]
data = [1,1,1]

A = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(3, 2)).tocsc()
print A.todense()

C = S.dot(A)
print C.todense()

counts = np.squeeze(np.asarray(A.sum(0)))
print counts

print C / counts



col = [0, 2, 3, 0, 2, 3, 4, 1, 2, 3, 4, 3, 0, 1, 4]
row = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4]
data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

df = coo_matrix((np.ones(len(row)), (np.array(row), np.array(col))), shape=(5000, 5))

print '-------------------------------'
print df.getcol(2).transpose().dot(df.getcol(2))[0,0]
print '-------------------------------'

from KMeans import KMeans

kmeans = KMeans(df, 2)

# kmeans.fit()
# print kmeans.labels
