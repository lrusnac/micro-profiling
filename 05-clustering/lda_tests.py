import sys
import numpy as np
import sklearn.decomposition as dec

if __name__ == '__main__':
    # dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 3, 10, 11), dtype=None, names=True, comments='@')
    dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 10, 11), dtype=None, skip_header=1, comments='@')

    print dataset

    lda = dec.LatentDirichletAllocation(n_jobs=-1).fit(dataset)
    print lda
    print lda.components_
