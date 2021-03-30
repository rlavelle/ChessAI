# Case-based reasoning backbone for related operations
# Zach Wilkerson, Rowan Lavelle, Josep Han

import sys
import math

class Feature:

    def __init__(self, value, name:str, similarityFunc):
        self.name = name
        self.value = value
        self.similarity = similarityFunc
        # self.weight = ?

    def __hash__(self):
        return hash(self.name)

    def getValue(self):
        return self.value

class Case:

    def __init__(self, output = None):
        self.features = {}
        self.output = output

    def addFeature(self, feature:Feature):
        self.features[hash(feature)] = feature

    def getFeature(self, featureName:str):
        return self.features[featureName]

    def getOutput(self):
        return self.output

    def getDifference(self, otherCase:Case):
        differences = {}
        for featureName in self.features.keys():
            differences[featureName] = self.features[featureName].similarity(otherCase.features[featureName])
        return differences

    def adapt(self, adaptationFunc):
        self.output = adaptationFunc(self.getOutput())

class CaseBase:
    
    def __init__(self):
        self.cases = {}
    
    def retrieve(self, caseKey):
        try:
            return self.cases[caseKey]
        except:
            print("That case does not exist")
            return

    def addCase(self, case:Case):
        self.cases[hash(case)] = case

    def getCase(self, caseKey):
        return self.cases[caseKey]

    def getKNN(self, k:int, query:Case):
        neighbors = [(None,sys.maxsize)] * k
        for caseHash in self.cases.keys():
            distance = 0.0
            differences = query.getDifference(self.getCase(caseHash))
            for elem in differences:
                distance += elem ** 2
            # distance = math.sqrt(distance)
            if distance < neighbors[k-1][1]:
                neighbors[k-1] = (caseHash, distance)
                neighbors.sort(key=lambda x:x[1])
        return neighbors