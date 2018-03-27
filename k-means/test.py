from kmeans import *
from numpy import *

if __name__ =='__main__':
    '''
    with open("seeds_dataset.txt") as f:
        dataset = [[float(x) for x in line.split('\t') if x != ''] for line in f]

    for i in dataset:
        del i[-1]
        print i

    file = open("seeds", 'w+')
    for tuple in dataset:
        s = ','.join(str(s) for s in tuple)
        file.write(s)
        file.write('\n')
    file.close()
    '''

    with open("iris") as f:
        dataset = [[float(x) for x in line.split(',') if x != ''] for line in f]
    for i in range(2,11):
        centroids, clusterData = kmeans(dataset, i, equaCentroids, manhattan)
        print  i, '\t', sum(clusterData, axis=0)[0,1]

