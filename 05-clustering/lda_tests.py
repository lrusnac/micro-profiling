import sys
import numpy as np
import sklearn.decomposition as dec

if __name__ == '__main__':
    # dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 3, 10, 11), dtype=None, names=True, comments='@')
    dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 10, 11), dtype=None, skip_header=1, comments='@')

    print dataset

    lda = dec.LatentDirichletAllocation(n_jobs=-1, learning_method='batch', verbose=3, max_iter=1)

    print 'lda creates, starting fit'

    lda.fit(dataset)

    print 'fit finished'

    print lda
    print lda.components_

    model = lda
    feature_names = ['year', 'hour', 'day']
    n_top_words = 20
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
