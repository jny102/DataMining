# Written by Ningyuan Jiang

import sys
import c45
import bayes

if __name__ =='__main__':
    with open("mushroom.training") as f:
        dataset = [[str(x) for x in line.split()] for line in f]
    with open("mushroom.test") as f:
        testData = [[str(x) for x in line.split()] for line in f]

    #print C45.splitFeature(dataset)
    dicts, classProb = bayes.computeProbs(dataset)
    testData = bayes.classify(testData, dicts, classProb)
    for i in testData:
        print i