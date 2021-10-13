from ruleobjects import RuleItem, FrequentRuleitems, Cars, CarsWithPruning

def join(item1, item2, dataset):
    if item1.classLabel != item2.classLabel:
        return None
    category1 = set(item1.condSet)
    category2 = set(item2.condSet)
    if category1 == category2:
        return None
    intersect = category1 & category2
    for item in intersect:
        if item1.condSet[item] != item2.condSet[item]:
            return None
    category = category1 | category2
    newCondSet = dict()
    for item in category:
        if item in category1:
            newCondSet[item] = item1.condSet[item]
        else:
            newCondSet[item] = item2.condSet[item]
    newRuleItem = RuleItem(newCondSet, item1.classLabel, dataset)
    return newRuleItem


def generateCandidate(frequentRuleitems, dataset):
    frequentRuleItemsToReturn = FrequentRuleitems()
    for item1 in frequentRuleitems.frequentRuleitemsSet:
        for item2 in frequentRuleitems.frequentRuleitemsSet:
            newRuleItem = join(item1, item2, dataset)
            if newRuleItem:
                frequentRuleItemsToReturn.add(newRuleItem)
                if (
                    frequentRuleItemsToReturn.getSize() >= 1000
                ):  # not allow to store more than 1000 ruleitems
                    return frequentRuleItemsToReturn
    return frequentRuleItemsToReturn


def ruleGenerator(dataset, minsup, minconf):
    frequentRuleitems = FrequentRuleitems()
    classAssociationRules = Cars()

    classLabel = set(
        [x[-1] for x in dataset]
    )  # this is the types of classification based on last column of dataset

    for column in range(
        len(dataset[0]) - 1
    ):  # loop all the columns except last since the last column is the classification label
        distinct_value = set(
            [x[column] for x in dataset]
        )  # distinct value for each column in the dataset
        for value in distinct_value:
            cond_set = {column: value}
            for classes in classLabel:
                ruleItem = RuleItem(cond_set, classes, dataset)
                if ruleItem.support >= minsup:
                    frequentRuleitems.add(ruleItem)

    classAssociationRules.genRules(frequentRuleitems, minsup, minconf)
    cars = classAssociationRules

    prevCarsNum = 0
    currentCarsNumber = len(cars.rules)

    while (
        frequentRuleitems.getSize() > 0
        and currentCarsNumber <= 2000
        and (currentCarsNumber - prevCarsNum) >= 10
    ):
        candidate = generateCandidate(frequentRuleitems, dataset)
        frequentRuleitems = FrequentRuleitems()
        classAssociationRules = Cars()
        for item in candidate.frequentRuleitemsSet:
            if item.support >= minsup:
                frequentRuleitems.add(item)
        classAssociationRules.genRules(frequentRuleitems, minsup, minconf)
        cars.append(classAssociationRules, minsup, minconf)

        prevCarsNum = currentCarsNumber
        currentCarsNumber = len(cars.rules)

    return classAssociationRules


def ruleGeneratorWithPruning(dataset, allRules):
    carsToPrune = CarsWithPruning(allRules)
    carsToPrune.pruneRules(dataset)
    return carsToPrune
