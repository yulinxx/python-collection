# https://github.com/georgekli/KMeans-DbScan
# 密度聚类方法的指导思想： 只要样本点的密度大于某阈值，则将该样本添加到最近的簇中。
# DBSCAN(Density based spatial clustering of applications with noise ), 将簇定义为密度相连的点的最大集合，能够把具有足够高密度的区域划分为簇，并可在有“噪声”的数据中发现任意形状的聚类。
# 密度聚类算法： DBSCAN 密度最大值算法
# 优点：
# (1) 能克服基于距离的算法只能发现“类圆形”（凸）的聚类的缺点，可发现任意形状的聚类。
# 比如：GMM——K-Means只能得到类圆形区域

# (2) 对噪声数据不敏感
# (3) 对数据的分布没有要求。（K-Means要求数据服从混合高斯分布）

# 缺点：
# (1) 计算密度单元的计算复杂度大，需要建立空间索引来降低计算量。
# https://blog.csdn.net/zhao_crystal/article/details/120834286

import sklearn
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
########################################
# 1.1 Do k-means clustering on some dimensions of iris dataset
########################################
if __name__ == '__main__':
    meas = load_iris().data
    # We initially use the last 2 data columns
    X = meas[:, [2, 3]]
    k = 3  # We need to do 3 class clustering
    # init = "random" # Test random initial centroids
    kmeans = KMeans(n_clusters=k).fit(X)  # Do k-means algorithm
    IDX = kmeans.labels_ # Get the labels of the clusters calculated
    C = kmeans.cluster_centers_ # Get the cluster centers
    plt.figure(1)
    # Plot the data indexes as clusters
    plt.plot(IDX[:], 'o')
    plt.show()
    # Plot the centroids and data in scatter
    plt.plot(X[IDX == 0][:, 0], X[IDX == 0][:, 1], 'limegreen', marker='o', linewidth=0, label='C1')
    plt.plot(X[IDX == 1][:, 0], X[IDX == 1][:, 1], 'yellow', marker='o', linewidth=0, label='C2')
    plt.plot(X[IDX == 2][:, 0], X[IDX == 2][:, 1], 'c.', marker='o', label='C3')
    plt.scatter(C[:, 0], C[:, 1], marker='x', color='black', s=150, linewidth=3, label="Centroids", zorder=10)
    plt.legend()
    plt.show()
    # Calculate Sum of Squered Errors
    SSE = kmeans.inertia_
    print("SSE is:", SSE)
    # Calculate Silouhette score
    sil = sklearn.metrics.silhouette_score(X, IDX)
    print("Silhouette score is:", sil)

    # Try to examine the k and SSE as well as k and SilScore function
    SSEs = [0] * 20
    SILs = [0] * 20
    for i in range(2, 20):
        # Do the same clustering for variable ks 2 to 10
        X = meas[:, [1, 3]]
        k = i
        kmeans = KMeans(n_clusters=k).fit(X)
        IDX = kmeans.labels_  # Get the labels of the clusters calculated
        # Calculate Metrics
        SSE = kmeans.inertia_
        sil = sklearn.metrics.silhouette_score(X, IDX)
        SSEs[i] = SSE
        SILs[i] = sil
    # Show results of SSE and k as well as SilScore and k
    plt.figure(2)
    plt.plot(range(2, 20), SSEs[2:20], 'go-', label='line 1', linewidth=2)
    plt.title("SSE(k)")
    plt.xlabel("k-clusters used")
    plt.ylabel("SSE")
    plt.show()
    plt.figure(3)
    plt.plot(range(2, 20), SILs[2:20], 'go-', label='line 1', linewidth=2)
    plt.title("Silhouette_Score(k)")
    plt.xlabel("k-clusters used")
    plt.ylabel("Silhouette score")
    plt.show()