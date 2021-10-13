from classifier import isSatisfy


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

    # print all the rules in the CARs
    def printRules(self):
        for rules in self.rules:
            rules.printRule()

    # add in a new ruleItem into the CARs if item support and confidence meets requirements
    def _add(self, ruleItem, minsup, minconf):
        if ruleItem.support >= minsup and ruleItem.confidence >= minconf:
            if ruleItem in self.rules:
                return
            for item in self.rules:
                if (
                    item.condSet == ruleItem.condSet
                    and item.confidence < ruleItem.confidence
                ):
                    self.rules.remove(item)
                    self.rules.add(ruleItem)
                    return
                elif (
                    item.condSet == ruleItem.condSet
                    and item.confidence >= ruleItem.confidence
                ):
                    return
            self.rules.add(ruleItem)

    # generate rules
    def genRules(self, frequentRuleitems, minsup, minconf):
        for item in frequentRuleitems.frequentRuleitemsSet:
            self._add(item, minsup, minconf)

    # add rules from new CARs into rules list
    def append(self, car, minsup, minconf):
        for item in car.rules:
            self._add(item, minsup, minconf)


class CarsWithPruning(Cars):
    def __init__(self, cars):
        Cars.__init__(self)
        self.rules = cars.rules
        self.prunedRules = set()

    def printPrunedRules(self):
        for rules in self.prunedRules:
            rules.printRule()

    # prune rules
    def pruneRules(self, dataset):
        # go through the rules in cars one by one to check if it satisfies the pruning condition
        for rule in self.rules:
            prunedRule = prune(rule, dataset)  # pruning method
            # to check if the pruned rules is repeated
            is_existed = False
            for rule in self.prunedRules:
                if rule.classLabel == prunedRule.classLabel:
                    if rule.condSet == prunedRule.condSet:
                        is_existed = True
                        break

            if not is_existed:
                self.prunedRules.add(prunedRule)

        self.rules = self.prunedRules


# Pruning method
def prune(rule, dataset):
    prunedRule = rule
    minRuleError = 9999999999  # just needs to be a large number, will get updated after 1 iteration of the function
    pruneRepetition = 0
    # prune rule recursively - remove attributes that are redundant
    # pruneRepetition > 10 stop prune --> to prevent infinite recursion
    def findPruneRule(thisRule):
        nonlocal prunedRule
        nonlocal minRuleError
        nonlocal pruneRepetition
        
        # calculate how many errors the rule r make in the dataset
        def ruleErrors(r):
            numOfErrors = 0
            for case in dataset:
                if isSatisfy(case, r) == False:
                    numOfErrors += 1
            return numOfErrors

        numOfErrors = ruleErrors(thisRule)
        if numOfErrors < minRuleError:
            minRuleError = numOfErrors
            prunedRule = thisRule

        condSetThisrule = list(thisRule.condSet)
        # print(condSetThisrule)



        if len(condSetThisrule) >= 2:
            # create a temporary rule without each attribute and check for errors, after each recursion,
            # remove one attribute of the rule and repeat until the rule has less than 2 attributes
            for attribute in condSetThisrule:
                tempCondSet = dict(thisRule.condSet)
                tempCondSet.pop(attribute)
                tempRule = RuleItem(tempCondSet, thisRule.classLabel, dataset)
                tempRuleRrror = ruleErrors(tempRule)
                if tempRuleRrror <= minRuleError:
                    minRuleError = tempRuleRrror
                    prunedRule = tempRule
                    if len(tempCondSet) >= 3:
                                # if 
                        if pruneRepetition >= 10:
                            return
                        pruneRepetition += 1
                        findPruneRule(tempRule)

    findPruneRule(rule)
    return prunedRule
