# https://github.com/georgekli/KMeans-DbScan
import scipy.io
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
########################################
# 1.2 Do k-means clustering on data of xV.mat
########################################
if __name__ == '__main__':
    # Load data xV.mat
    mat_file = scipy.io.loadmat('xV.mat')
    xV = np.array(mat_file['xV'])

    # K-means on the first 2 data columns
    #####################################
    X = xV[:,[0,1]]
    # Make 3 clusters
    k = 3
    kmeans = KMeans(n_clusters=k).fit(X)
    # Get k-means results
    IDX = kmeans.labels_
    C = kmeans.cluster_centers_
    # Plot centroids and data
    plt.plot(X[IDX==0][:,0], X[IDX==0][:,1], 'limegreen', marker='o', linewidth=0, label='C1')
    plt.plot(X[IDX==1][:,0], X[IDX==1][:,1], 'yellow', marker='o', linewidth=0, label='C2')
    plt.plot(X[IDX==2][:,0], X[IDX==2][:,1], 'c.', marker='o', label='C3')
    plt.scatter(C[:,0], C[:,1], marker='x', color='black', s=150 , linewidth=3, label="Centroids", zorder=10)
    plt.legend()
    plt.title("features 0, 1")
    plt.show()
    # Calculate Sum of Square errors
    SSE = kmeans.inertia_
    print("K-means on col 0 and 1, SSE is:", SSE)

    # K-means on the 296 and 305 data columns
    #####################################
    X = xV[:,[296, 305]]
    kmeans = KMeans(n_clusters=k).fit(X)
    IDX = kmeans.labels_
    C = kmeans.cluster_centers_
    plt.plot(X[IDX==0][:,0], X[IDX==0][:,1], 'limegreen', marker='o', linewidth=0, label='C1')
    plt.plot(X[IDX==1][:,0], X[IDX==1][:,1], 'yellow', marker='o', linewidth=0, label='C2')
    plt.plot(X[IDX==2][:,0], X[IDX==2][:,1], 'c.', marker='o', label='C3')
    plt.scatter(C[:,0], C[:,1], marker='x', color='black', s=150 , linewidth=3, label="Centroids", zorder=10)
    plt.legend()
    plt.title("features 296, 305")
    plt.show()
    SSE = kmeans.inertia_
    print("K-means on col 296 and 305, SSE is:", SSE)

    # K-means on the last 2 data columns
    #####################################
    X = xV[:, [467, 468]]
    kmeans = KMeans(n_clusters=k).fit(X)
    IDX = kmeans.labels_
    C = kmeans.cluster_centers_
    plt.plot(X[IDX == 0][:, 0], X[IDX == 0][:, 1], 'limegreen', marker='o', linewidth=0, label='C1')
    plt.plot(X[IDX == 1][:, 0], X[IDX == 1][:, 1], 'yellow', marker='o', linewidth=0, label='C2')
    plt.plot(X[IDX == 2][:, 0], X[IDX == 2][:, 1], 'c.', marker='o', label='C3')
    plt.scatter(C[:, 0], C[:, 1], marker='x', color='black', s=150, linewidth=3, label="Centroids", zorder=10)
    plt.legend()
    plt.title("features 467, 468")
    plt.show()
    SSE = kmeans.inertia_ 
    print("K-means on col 467 and 468, SSE is:", SSE)

    # K-means on the 205 and 175 data columns
    #####################################
    X = xV[:, [205, 175]]
    kmeans = KMeans(n_clusters=k).fit(X)
    IDX = kmeans.labels_
    C = kmeans.cluster_centers_
    plt.plot(X[IDX == 0][:, 0], X[IDX == 0][:, 1], 'limegreen', marker='o', linewidth=0, label='C1')
    plt.plot(X[IDX == 1][:, 0], X[IDX == 1][:, 1], 'yellow', marker='o', linewidth=0, label='C2')
    plt.plot(X[IDX == 2][:, 0], X[IDX == 2][:, 1], 'c.', marker='o', label='C3')
    plt.scatter(C[:, 0], C[:, 1], marker='x', color='black', s=150, linewidth=3, label="Centroids", zorder=10)
    plt.legend()
    plt.title("features 205, 175")
    plt.show()
    SSE = kmeans.inertia_
    print("K-means on col 205 and 175, SSE is:", SSE)