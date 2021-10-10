class Classifier:
    def __init__(self):
        self.ruleList = list()
        self.defaultClass = None
        self._errorList = list()
        self._defaultClassList = list()

    # insert a rule into rule_list, then choose a default class, and calculate the errors (see line 8, 10 & 11)
    def insert(self, rule, dataset):
        self.ruleList.append(rule)  # insert r at the end of C
        self._selectDefaultClass(dataset)  # select a default class for the current C
        self._computeError(dataset)  # compute the total number of errors of C

    # select the majority class in the remaining data
    def _selectDefaultClass(self, dataset):
        classColumn = [x[-1] for x in dataset]
        classLabel = set(classColumn)
        max = 0
        currentDefaultClass = None
        for label in classLabel:
            if classColumn.count(label) >= max:
                max = classColumn.count(label)
                currentDefaultClass = label
        self._defaultClassList.append(currentDefaultClass)

    # compute the sum of errors
    def _computeError(self, dataset):

        error_number = 0

        # the number of errors that have been made by all the selected rules in C
        for case in dataset:
            is_cover = False
            for rule in self.ruleList:
                if isSatisfy(case, rule):
                    is_cover = True
                    break
            if not is_cover:
                error_number += 1

        # the number of errors to be made by the default class in the training set
        class_column = [x[-1] for x in dataset]
        error_number += len(class_column) - class_column.count(
            self._defaultClassList[-1]
        )
        self._errorList.append(error_number)

    # see line 14 and 15, to get the final classifier
    def discard(self):
        # find the first rule p in C with the lowest total number of errors and drop all the rules after p in C
        index = self._errorList.index(min(self._errorList))
        self.ruleList = self.ruleList[: (index + 1)]
        self._errorList = None

        # assign the default class associated with p to default_class
        self.defaultClass = self._defaultClassList[index]
        self._defaultClassList = None

    # just print out all selected rules and default class in our classifier
    def print(self):
        for rule in self.ruleList:
            rule.printRule()
        print("Classifier Default Class:", self.defaultClass)


def isSatisfy(datacase, rule):
    for item in rule.condSet:
        if datacase[item] != rule.condSet[item]:
            return None
    if datacase[-1] == rule.classLabel:
        return True
    else:
        return False


# sort the set of generated rules car according to the relation ">", return the sorted rule list
def sort(car):
    def compareMethod(a, b):
        if a.confidence < b.confidence:  # 1. the confidence of ri > rj
            return 1
        elif a.confidence == b.confidence:
            if (
                a.support < b.support
            ):  # 2. their confidences are the same, but support of ri > rj
                return 1
            elif a.support == b.support:
                if len(a.condSet) < len(
                    b.condSet
                ):  # 3. both confidence & support are the same, ri earlier than rj
                    return -1
                elif len(a.condSet) == len(b.condSet):
                    return 0
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    ruleList = list(car.rules)
    ruleList.sort(key=compareToKey(compareMethod))
    return ruleList


def compareToKey(mycmp):
    class K(object):
        __slots__ = ["obj"]

        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        __hash__ = None

    return K


def classifierBuilder(cars, data):
    classifier = Classifier()
    carsList = sort(cars)
    for rule in carsList:
        temp = []
        mark = False
        for i in range(len(data)):
            isSatisfyValue = isSatisfy(data[i], rule)
            if isSatisfyValue is not None:
                temp.append(i)
                if isSatisfyValue:
                    mark = True
        if mark:
            temp_dataset = list(data)
            for index in temp:
                temp_dataset[index] = []
            while [] in temp_dataset:
                temp_dataset.remove([])
            data = temp_dataset
            classifier.insert(rule, data)
    classifier.discard()
    return classifier
