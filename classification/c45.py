# Written by Ningyuan Jiang

from math import log

import sys


def readData(input):
    with open(input) as f:
        dataset = [[str(x) for x in line.split()] for line in f]
    return dataset


def info(dataset):   # Information entropy
    numTuples, numLabels = len(dataset), dict()
    for tuple in dataset:
        label = tuple[0]   # The class label of this tuple
        if label in numLabels.keys():
            numLabels[label] += 1
        else:
            numLabels[label] = 1
    entropy = 0
    for label in numLabels.keys():
        p = float(numLabels[label]) / numTuples
        entropy -= p * log(p, 2)
    return entropy


def partition(dataset, feature, value):   # Partition the dataset given the specific value of a feature
    subset = list()
    for tuple in dataset:
        if tuple[feature] == value:
            newTuple = tuple[:]
            del newTuple[feature]
            subset.append(newTuple)
    return subset


def splitFeature(dataset, labels):
    entropy = info(dataset)
    bestRatio, bestFeature = float(0), 0   # Initialize variables for competition
    for feature in range(1,len(dataset[0])):   # Ignore the first column (class label)
        values = set(map(lambda tuple: tuple[feature], dataset))   # Set() because we want unique values
        featureEntropy, splitInfo = float(0), float(0)
        for value in values:
            subset = partition(dataset, feature, value)
            p = float(len(subset)) / len(dataset)   # Probability of this value
            featureEntropy += p * info(subset)
            splitInfo -= p * log(p, 2)
        gain = entropy - featureEntropy
        if splitInfo == 0:   # FIXME
            continue
        gainRatio = gain / splitInfo
        #gainRatio = gain
        if gainRatio > bestRatio:
            bestRatio, bestFeature = gainRatio, feature
    #if bestFeature == 0: bestFeature = labels[1];
    return bestFeature


def majority(classLabels):
    count = dict()
    for label in classLabels:
        if label in count.keys():
            count[label] += 1
        else:
            count[label] = 1
    return max(count, key=count.get)


def decisionTree(dataset, labels):   # Recursive function to create a decision tree
    classLabels = map(lambda tuple: tuple[0], dataset)   # Class labels are at the beginning of each tuple (given)
    if all(x == classLabels[0] for x in classLabels):   # All the class labels are the same, terminate
        return classLabels[0]
    if len(dataset[0]) == 1:
        return majority(classLabels)
    feature = splitFeature(dataset, labels)
    print labels, feature
    label = labels[feature]
    tree = {label:{}}
    del labels[feature]
    values = set(map(lambda tuple: tuple[feature], dataset))
    for value in values:
        subset = partition(dataset, feature, value)
        tree[label][value] = decisionTree(subset, labels)
    return tree


def writeFile(dataset, name):
    file = open(name, 'w+')
    for tuple in dataset:
        s = '\t'.join(str(s) for s in tuple)
        file.write(s)
        file.write('\n')
    file.close()


def computeAccuracy(testData):
    count = 0
    for tuple in testData:
        if tuple[0] == tuple[-1]:
            count += 1
    accuracy = count / float(len(testData))
    testData.insert(0, ['Accuracy is', accuracy])
    return testData


def c45(training, test):
    trainingData = readData(training)
    labels = list(range(0,len(trainingData[0])))
    tree = decisionTree(trainingData, labels)
    testData = readData(test)
    for tuple in testData:
        feature = list(tree.keys())[0]
        tempTree = tree
        while True:
            value = tuple[feature]
            child = tempTree[feature][value]
            if type(child).__name__ != 'dict':
                tuple.append(child)
                break
            else:
                tempTree = child
                feature = list(tempTree.keys())[0]
    testData = computeAccuracy(testData)
    return testData


if __name__ =='__main__':
    testData = c45(sys.argv[1], sys.argv[2])
    writeFile(testData, sys.argv[3])