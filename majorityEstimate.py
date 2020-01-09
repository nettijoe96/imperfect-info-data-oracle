import operator as op
from functools import reduce
import math


sample_size = None
updatedPriorsDict = None
combDict = None

cherryStr = "cherry"
limeStr = "lime"
undecidedStr = "undecided"

"""
estimates the majority, minority, and undecided buckets recursively. 
base case is when you assume that all voters vote
"""
def estimates(priors, percentCherry, rounds, r):
    majority = 0
    minority = 0
    undecided = 0
    if r == rounds:   # base condition
        for i in range(0, len(priors)):
            myMajority, myMinority, myUndecided = allVotersVoteEstimates(percentCherry[i])
            majority += priors[i] * myMajority
            minority += priors[i] * myMinority
            undecided += priors[i] * myUndecided
        if round(majority + minority + undecided, 3) != 1:
            print("sum of estimates not equal to 1:", majority+minority+undecided)
    else:
        # go through every "world possibility"
        for i in range(0, len(priors)):
            #print("prior", i)
            # go through every possible combination of data
            for cherries in range(0, sample_size+1):
                # update prior for that number of cherries/limes
                newPriors = updatedPriorsDict[str(cherries)]
                probCherry = getPi(newPriors, percentCherry)
                # get the estimates for these people
                myMajority, myMinority, myUndecided = estimates(newPriors, percentCherry, rounds, r+1)
                if profitable(probCherry, myMajority, myMinority):
                    majority += priors[i] * binomial(cherries, priors[i])
                elif profitable(1-probCherry, myMinority, myMajority):
                    minority += priors[i] * binomial(cherries, priors[i])
                else:
                    undecided += priors[i] * binomial(cherries, priors[i])
    return majority, minority, undecided
 


def binomial(cherries, percentCherry):
    percent = combDict[str(cherries)] * (percentCherry**cherries) * (1-percentCherry)**(sample_size-cherries)
    return percent

def profitable(prob, majority, minority):
    if majority == 0:
        return False
    if minority > majority:
        return False
    else:
        gain = prob * (minority/majority)
        loss = 1-prob
        return gain > loss

def updatePriors(cherries, limes, initialPriors, priorsCherryProb):
    priors = initialPriors
    for i in range(0, cherries):
        priorsUnscaled = []
        for j in range(0, len(priors)):
            priorsUnscaled += [priorsCherryProb[j] * priors[j]]
        s = sum(priorsUnscaled)
        for j in range(0, len(priors)):
            priors[j] = priorsUnscaled[j] / s
    for i in range(0, limes):
        priorsUnscaled = []
        for j in range(0, len(priors)):
            priorsUnscaled += [(1-priorsCherryProb[j]) * priors[j]]
        s = sum(priorsUnscaled)
        for j in range(0, len(priors)):
            priors[j] = priorsUnscaled[j] / s
    return priors


def getPi(priors, priorsCherryProb):
    prob = 0
    for j in range(0, len(priors)):
        prob += priorsCherryProb[j] * priors[j]
    return prob



def allVotersVoteEstimates(percentCherry):
    majority = 0
    minority = 0
    undecided = 0
    for cherries in range(0, sample_size+1):
        percent = binomial(cherries, percentCherry)
        if cherries < sample_size/2:
            minority += percent
        elif cherries > sample_size/2:
            majority += percent
        else:
            undecided += percent
    return majority, minority, undecided



def sumOfCherryVotersRound2(percentCherry, sample_size):
    totPercent = 0
    for cherries in range(math.floor(sample_size/2)+1, sample_size+1):
        comb = ncr(sample_size, cherries)
        percent = comb * (percentCherry**cherries) * (1-percentCherry)**(sample_size-cherries)
        totPercent += percent
    return totPercent


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom



def decide(observedCherries, sampleSize, rounds, initialPriors, priorsCherryProb):
    global sample_size, updatedPriorsDict, combDict
    sample_size = sampleSize
    combDict = makeCombDict(sampleSize)
    updatedPriorsDict = makeUpdatedPriorsDict(sampleSize, initialPriors, priorsCherryProb)
    observedLimes = sampleSize-observedCherries
    init = [p for p in initialPriors]
    myPriors = updatePriors(observedCherries, observedLimes, init, priorsCherryProb)
    #printPriors(myPriors, priorsCherryProb)
    majority, minority, undecided = estimates(myPriors, priorsCherryProb, rounds, 1)
    probCherry = getPi(myPriors, priorsCherryProb)
    #print("expectation of cherry", probCherry)
    #print("majority:", majority, "minority:", minority, "undecided", undecided)
    if profitable(probCherry, majority, minority):
        return cherryStr
    elif profitable(1-probCherry, minority, majority):
        return limeStr
    else:
        return undecidedStr


def makeUpdatedPriorsDict(sampleSize, initialPriors, priorsCherryProb):
    updatedPriorsDict = {}
    for cherries in range(0, sampleSize+1):
        init = [p for p in initialPriors]
        updatedPriorsDict[str(cherries)] = updatePriors(cherries, sampleSize-cherries, init, priorsCherryProb)
    return updatedPriorsDict


def makeCombDict(sampleSize):
    combDict = {}
    for cherries in range(0, sampleSize+1):
        comb = ncr(sampleSize, cherries)
        combDict[str(cherries)] = comb
    return combDict


def printPriors(priors, cherryProb):
    print("my priors: ", end="")
    print([round(p, 2) for p in priors])

def experimentHeaderPrint(rounds, sampleSize, initialPriors, priorsCherryProb, observedCherries):
    print("number of recursive rounds:", rounds)
    print("sample size:", sampleSize)
    print("initial priors mapping: ", end="")
    print(priorsCherryProb, " --> ", [round(p, 2) for p in initialPriors])

def main():
    rounds = 2
    sampleSize = 20
    observedCherries = 16
    initialPriors =    [1/5 for i in range(0, 5)]
    priorsCherryProb = [0, .2, .6, .8, 1]
    experimentHeaderPrint(rounds, sampleSize, initialPriors, priorsCherryProb, observedCherries)
    count = 0
    for cherries in range(0, sampleSize+1):
        print(cherries, "observed cherries")
        isProfitable = decide(cherries, sampleSize, rounds, initialPriors, priorsCherryProb)
        if isProfitable != undecidedStr:
            print(cherries, "is profitable")
            count += 1
        else:
            print("not profitable")
    if count == 0: 
        print("none are profitable")

main()
