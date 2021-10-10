class FrequentRuleitems:
    def __init__(self):
        self.frequentRuleitemsSet = set()

    # get size of set
    def getSize(self):
        return len(self.frequentRuleitemsSet)

    # add a new ruleitem into set
    def add(self, rule_item):
        is_existed = False
        for item in self.frequentRuleitemsSet:
            if item.classLabel == rule_item.classLabel:
                if item.condSet == rule_item.condSet:
                    is_existed = True
                    break
        if not is_existed:
            self.frequentRuleitemsSet.add(rule_item)

    # append set of ruleitems
    def append(self, sets):
        for item in sets.frequentRuleitems:
            self.add(item)

    # print out all frequent ruleitems
    def print(self):
        for item in self.frequentRuleitemsSet:
            item.printRule()


class RuleItem:
    # RuleItem : <condSet, y>, rule : condSet -> y , y is the classification
    # condsupCount = number of cases in dataset that contain the condSet
    # rulesupCount = number of cases in dataset that are have classification label y
    def __init__(self, condSet, classLabel, dataset):
        self.condSet = condSet
        self.classLabel = classLabel

        self.condsupCount, self.rulesupCount = self._getsupCount(dataset)
        self.support = self._getSupport(len(dataset))
        self.confidence = self._getConfidence()

    # calculate condsupCount and rulesupCount
    def _getsupCount(self, dataset):
        condsupCount = 0
        rulesupCount = 0

        # loop through dataset to check each row if the current condSet exists within the row
        for row in dataset:
            is_contained = True
            for index in self.condSet:
                if self.condSet[index] != row[index]:
                    is_contained = False
                    break
            if is_contained:  # condSet exist in the current row
                condsupCount += 1
                if self.classLabel == row[-1]:  # check if condSet -> y
                    rulesupCount += 1
        return condsupCount, rulesupCount

    # calculate support count
    def _getSupport(self, datasetSize):
        return self.rulesupCount / datasetSize

    # calculate confidence
    def _getConfidence(self):
        if self.condsupCount != 0:
            return self.rulesupCount / self.condsupCount
        else:
            return 0

    # print out rule with formatting so that condSet => y
    def printRule(self):
        condSetOutput = ""
        # format all the  condSets
        for item in self.condSet:
            condSetOutput += "(" + str(item) + ", " + str(self.condSet[item]) + "), "
        condSetOutput = "{" + condSetOutput[:-2] + "}"
        print(condSetOutput + " -> (class, " + str(self.classLabel) + ")")


class Cars:
    def __init__(self):
        self.rules = set()

    # print out all rules
    def printRules(self):
        for item in self.rules:
            item.printRule()

    # add a new rule (frequent & accurate), save the ruleitem with the highest confidence when having the same condset
    def _add(self, ruleItem, minsup, minconf):
        if ruleItem.support >= minsup and ruleItem.confidence >= minconf:
            if ruleItem in self.rules:
                return
            for item in self.rules:
                if item.condSet == ruleItem.condSet and item.confidence < ruleItem.confidence:
                    self.rules.remove(item)
                    self.rules.add(ruleItem)
                    return
                elif item.condSet == ruleItem.condSet and item.confidence >= ruleItem.confidence:
                    return
            self.rules.add(ruleItem)

    # convert frequent ruleitems into car
    def genRules(self, frequent_ruleitems, minsup, minconf):
        for item in frequent_ruleitems.frequentRuleitemsSet:
            self._add(item, minsup, minconf)

    # union new car into rules list
    def append(self, car, minsup, minconf):
        for item in car.rules:
            self._add(item, minsup, minconf)
