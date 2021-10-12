import time
import random
import reader
from rmep import split
from rulegenerator import ruleGenerator
from pre_proccessing2 import pre_process
from classifier import classifierBuilder, isSatisfy

# constants
minSup = 0.01
minConf = 0.5

# path to csv file
csvPath = "datasets/glass.csv"

# path to data/names
dataPath = "datasets/abalone.data"
namesPath = "datasets/abalone.names"

# classAtLastColumn is to check if the classificaiton label is at last column,
# if it is at first column, shift everything in first column to last later
classAtLastColumn = False


def prepareData():
    # read data

    # use this to read .csv
    # header, data, valueType = reader.readExcel(csvPath)

    # user this to read .data
    header, data, valueType = reader.readData(dataPath, namesPath)

    random.shuffle(data)
    # shift everything from first column to last
    if not classAtLastColumn:
        for row in data:
            toShift = row[0]
            row.pop(0)
            row.append(toShift)

        toShift = header[0]
        header.pop(0)
        header.append(toShift)

        valueType.pop(0)
        valueType.append("label")
    else:
        valueType[-1] = "label"

    data = pre_process(data, header, valueType)

    return data


def generateRules(data):
    startTime = time.time()
    rules = ruleGenerator(data, minSup, minConf)
    endTime = time.time()
    timeTaken = endTime - startTime
    print("Rules:")
    rules.printRules()
    print("Time taken to generate rules: %.2lf s" % (timeTaken / 10))
    return rules


def buildClassifier(rules, data):
    startTime = time.time()
    classifier = classifierBuilder(rules, data)
    endTime = time.time()
    timeTaken = endTime - startTime
    print("Time taken to build classifier: %.2lf s" % (timeTaken / 10))
    return classifier


def getAccuracy(classifier, dataset):
    size = len(dataset)
    numberOfErrors = 0
    for case in dataset:
        isSatisfyValue = False
        for rule in classifier.ruleList:
            isSatisfyValue = isSatisfy(case, rule)
            if isSatisfyValue == True:
                break
        if isSatisfyValue == False:
            if classifier.defaultClass != case[-1]:
                numberOfErrors += 1
    accuracy = 1 - (numberOfErrors / size)
    return accuracy


def runValidate():
    data = prepareData()
    # print(data)
    # to split for train and test
    splitPoint = round(0.8 * len(data))
    trainData = data[:splitPoint]
    testData = data[splitPoint:]

    rules = generateRules(trainData)

    classifier = buildClassifier(rules, trainData)

    accuracy = getAccuracy(classifier, testData) * 100
    accuracyString = "Accuracy: " + str(round(accuracy, 2)) + "%"
    print(accuracyString)


if __name__ == "__main__":
    runValidate()
