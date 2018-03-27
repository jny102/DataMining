# Written by Ningyuan Jiang

import sys
from collections import OrderedDict


def readData(input):
    with open(input) as f:
        dataset = [[str(x) for x in line.split()] for line in f]
    return dataset


def computeProbs(dataset):   # Return two lists that contains every possibility that may be used
    feature_value = {}
    for i in range(1, len(dataset[0])):
        feature_value[i] = list(set(map(lambda tuple: tuple[i], dataset)))
    classes = list(set(map(lambda tuple: tuple[0], dataset)))
    numFeatures = len(dataset[0]) - 1
    subsets = []
    classProb = OrderedDict()
    for i in range(len(classes)):
        subset = filter(lambda x: x[0] == classes[i], dataset)
        subsets.append(subset)
        classProb[classes[i]] = len(subset) / float(len(dataset))
    dicts = []   # listOfClasses(dictOfFeature(dictOfValues))
    for i in range(len(subsets)):
        subset = subsets[i]
        length = float(len(subset))
        dicts.append(dict())
        classDict = dicts[i]
        for feature in range(1, numFeatures+1):   # From the first feature to the last one
            featureDict = classDict[feature] = {}
            for tuple in subset:
                value = tuple[feature]
                if value not in featureDict.keys():
                    featureDict[value] = 1
                else:
                    featureDict[value] += 1
            for value in featureDict.keys():
                featureDict[value] += 1   # Laplacian correction
                featureDict[value] /= length
            for value in feature_value[feature]:
                if value not in featureDict.keys():
                    featureDict[value] = 1 / length   # Laplacian correction
    return dicts, classProb


def classify(testData, dicts, classProb):
    for tuple in testData:
        p_x = []
        for c in range(len(classProb)):
            p_x.append(float(1))
            for feature in range(1, len(tuple)):
                value = tuple[feature]
                p_x[c] *= dicts[c][feature][value]
            p_x[c] *= classProb.items()[c][1]
        index = p_x.index(max(p_x))
        tuple.append(classProb.items()[index][0])
    return testData


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


def bayes(training, test):
    trainingData, testData = readData(training), readData(test)
    dicts, classProb = computeProbs(trainingData)
    testData = classify(testData, dicts, classProb)
    testData = computeAccuracy(testData)
    return testData

if __name__ =='__main__':
    testData = bayes(sys.argv[1], sys.argv[2])
    writeFile(testData, sys.argv[3])