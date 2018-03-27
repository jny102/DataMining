# Written by Ningyuan Jiang

import math
import sys
import random
from numpy import *

def readData(input):
    with open(input) as f:
        dataset = [[float(x) for x in line.split(',')] for line in f]
    return dataset


def euclidean(a, b):
    dist = 0
    for i in range(len(a)):
        dist += (a[i] - b[i]) ** 2
    return math.sqrt(dist)


def manhattan(a, b):
    dist = 0
    for i in range(len(a)):
        dist += abs(a[i] - b[i])
    return dist


def randomize(dataset, k):
    centroids = []
    n = len(dataset[0])   # Number of attributes
    maxV = [max(x[i] for x in dataset) for i in range(n)]
    minV = [min(x[i] for x in dataset) for i in range(n)]
    for i in range(k):
        centroids.append([random.uniform(minV[j], maxV[j]) for j in range(n)])
    return centroids


def equaCentroids(dataset, k):
    n = len(dataset[0])  # Number of attributes
    maxV = [max(x[i] for x in dataset) for i in range(n)]
    minV = [min(x[i] for x in dataset) for i in range(n)]
    centroids = [maxV, minV]
    part = float(k - 1)   # No. of equa-distance part
    seg = [(x - y)/part for x,y in zip(maxV, minV)]
    for i in range(k-2):
        centroids.append([x + y for x, y in zip(centroids[-1], seg)])
    return centroids


def kmeans(dataset, k, centroidEngine, distEngine):
    centroids = centroidEngine(dataset, k)
    clusterData = mat(zeros((len(dataset),2)))   # 1st column: its cluster no., 2nd col: error
    notConverged = True
    while notConverged:
        notConverged = False
        for i in range(len(dataset)):
            minDistance, index = inf, -inf
            for j in range(k):
                distance = distEngine(dataset[i], centroids[j])   # i is the tuple in dataset, j in centroids
                if distance < minDistance:
                    minDistance, index = distance, j
            if clusterData[i,0] != index:
                notConverged = True
            clusterData[i,:] = index, pow(minDistance, 2)   # Store the information, cluster and error
        #print centroids
        for c in range(k):
            tempSet = []
            for i in range(len(dataset)):
                if clusterData[i,0] == c:
                    tempSet.append(dataset[i])
            if len(tempSet) == 0:
                #centroids[c] = [inf for x in centroids[c]]
                continue
            tempMat = mat(tempSet)
            centroid = []
            for j in range(len(dataset[0])):
                centroid.append(mean(tempMat[:,j]))
            centroids[c] = centroid
    return centroids, clusterData


def writeFile(dataset, name):
    file = open(name, 'w+')
    for tuple in dataset:
        s = '\t'.join(str(s) for s in tuple)
        file.write(s)
        file.write('\n')
    file.close()


def calculateSSE(clusterData):
    sse = sum(clusterData, axis=0)[0,1]
    return "SSE = " + str(sse)


if __name__ =='__main__':
    dataset = readData(sys.argv[1])
    centroids, clusterData = kmeans(dataset, int(sys.argv[2]), equaCentroids, euclidean)
    dataset = [x + [int(clusterData[dataset.index(x), 0])] for x in dataset]
    dataset.append([calculateSSE(clusterData)])
    writeFile(dataset, sys.argv[3])