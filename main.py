import random
import reader
from datetime import datetime
from rulegenerator import ruleGenerator, ruleGeneratorWithPruning
from pre_proccessing2 import pre_process
from classifier import classifierBuilder, isSatisfy

# constants
minSup = 0.01
minConf = 0.5

## paths to csv file
# csvPath = "datasets/glass.csv" # class last column = true

# csvPath = "datasets/internetfirewall.csv" # class last column = false

# csvPath = "datasets/mushrooms.csv" # class last column = false

## paths to data/names
# dataPath = "datasets/abalone.data" # class last column = false
# namesPath = "datasets/abalone.names"

# dataPath = "datasets/car.data" # class last column = true
# namesPath = "datasets/car.names"

dataPath = "datasets/heart.dat" # class last column = true
namesPath = "datasets/heart.names"

# dataPath = "datasets/breast-cancer.data" # class last column = false
# namesPath = "datasets/breast-cancer.names"

# dataPath = "datasets/balance-scale.data"  # class last column = false
# namesPath = "datasets/balance-scale.names"


# classAtLastColumn is to check if the classificaiton label is at last column,
# if it is at first column, shift everything in first column to last later
classAtLastColumn = True


def formatMicroSeconds(microS):
    strSeconds = str(microS/1000000) + " seconds"
    return strSeconds


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
    print("Generating rules...")
    startTime = datetime.now()
    rules = ruleGenerator(data, minSup, minConf)
    endTime = datetime.now()
    timeTaken = endTime - startTime
    print("Rules generated.")
    formatMicroSeconds(1000)
    print("Time taken to generate rules:", formatMicroSeconds(timeTaken.microseconds))
    return rules


def generateRulesWithPruning(dataset, allCars):
    print("Pruning rules...")
    startTime = datetime.now()
    rulesWithPruning = ruleGeneratorWithPruning(dataset, allCars)
    endTime = datetime.now()
    timeTaken = endTime - startTime
    print("Rules pruned.")
    print("Time taken to prune rules:", formatMicroSeconds(timeTaken.microseconds))
    return rulesWithPruning


def buildClassifier(rules, data, isPrunedData):
    print("Building classifier...")
    startTime = datetime.now()
    classifier = classifierBuilder(rules, data)
    endTime = datetime.now()
    timeTaken = endTime - startTime
    print("Classifier built.")
    if isPrunedData:
        print(
            "Time taken to build classifier WITH pruning:",
            formatMicroSeconds(timeTaken.microseconds),
        )
    else:
        print(
            "Time taken to build classifier WITHOUT pruning:",
            formatMicroSeconds(timeTaken.microseconds),
        )
    return classifier


def getAccuracy(classifier, dataset, isPrunedData):
    startTime = datetime.now()
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
    endTime = datetime.now()
    timeTaken = endTime - startTime
    if isPrunedData:
        print(
            "Time taken to calculate accuracy of classifier WITH pruning:",
            formatMicroSeconds(timeTaken.microseconds),
        )
    else:
        print(
            "Time taken to calculate accuracy of classifier WITHOUT pruning:",
            formatMicroSeconds(timeTaken.microseconds),
        )
    return accuracy


def runValidate():
    data = prepareData()
    # to split for train and test
    splitPoint = round(0.8 * len(data))
    trainData = data[:splitPoint]
    testData = data[splitPoint:]

    rules = generateRules(trainData)
    rulesWithPruning = generateRulesWithPruning(trainData, rules)

    print("Number of rules WITHOUT pruning:", len(rules.rules))
    print("Number of rules WITH pruning:", len(rulesWithPruning.rules))
    print("")
    classifier = buildClassifier(rulesWithPruning, trainData, False)

    classifierWithPrunedRules = buildClassifier(rulesWithPruning, trainData, True)
    print("")
    accuracy = getAccuracy(classifier, testData, False) * 100
    accuracyString = (
        "Accuracy of classifier WITHOUT pruning: " + str(round(accuracy, 2)) + "%"
    )
    print(accuracyString)

    accuracyWithPruning = getAccuracy(classifierWithPrunedRules, testData, True) * 100
    accuracyStringWithPruning = (
        "Accuracy of classifier WITH pruning: "
        + str(round(accuracyWithPruning, 2))
        + "%"
    )
    print(accuracyStringWithPruning)
    print("")


if __name__ == "__main__":
    runValidate()
