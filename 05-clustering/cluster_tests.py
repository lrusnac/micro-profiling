import sys
import numpy as np
import sklearn.cluster as cl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")

if __name__ == '__main__':
    # dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 3, 10, 11), dtype=None, names=True, comments='@')
    dataset = np.genfromtxt(sys.argv[1], delimiter=';', usecols=(2, 10, 11), dtype=None, skip_header=1, comments='@')

    print dataset

    kmeans = cl.KMeans(n_jobs=-1).fit(dataset)
    print kmeans
    print kmeans.labels_
    print kmeans.cluster_centers_

    colors = 10*['r','g','b','c','k','y','m']
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    print(colors)
    print(labels)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(dataset)):
        ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], c=colors[labels[i]], marker='o')


    ax.scatter(cluster_centers[:,0],cluster_centers[:,1],cluster_centers[:,2],
                marker="x",color='k', s=150, linewidths = 5, zorder=10)

    plt.savefig('test.png')
