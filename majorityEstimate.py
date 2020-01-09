import operator as op
from functools import reduce
import math

"""
estimates the majority, minority, and undecided buckets recursively. 
base case is when you assume that all voters vote
"""
def estimates(priors, percentCherry, r):
    majority = 0
    minority = 0
    undecided = 0
    if r == rounds:   # base condition
        for i in range(0, len(priors)):
            myMajority, myMinority, myUndecided = allVotersVoteEstimates(percentCherry[i])
#            print("in base:", myMajority, myMinority, myUndecided)
            majority += priors[i] * myMajority
            minority += priors[i] * myMinority
            undecided += priors[i] * myUndecided
        if round(majority + minority + undecided, 3) != 1:
            print("sum of estimates not equal to 1:", majority+minority+undecided)
    #    print(r, ":", majority, minority, undecided)
    else:
        # go through every "world possibility"
        for i in range(0, len(priors)):
            print("prior", i)
            # go through every possible combination of data
            for cherries in range(0, sampleSize+1):
                # update prior for that number of cherries/limes
                newPriors = updatedPriorsDict[str(cherries)]
                probCherry = getPi(newPriors, percentCherry)
#                print("newPriors", newPriors)
#                print("probCherry", probCherry)
                # get the estimates for these people
                myMajority, myMinority, myUndecided = estimates(newPriors, percentCherry, r+1)
#                print(r, ":", myMajority, myMinority, myUndecided)
                if profitable(probCherry, myMajority, myMinority):
                    majority += priors[i] * binomial(cherries, priors[i])
                elif profitable(1-probCherry, myMinority, myMajority):
                    minority += priors[i] * binomial(cherries, priors[i])
                else:
                    undecided += priors[i] * binomial(cherries, priors[i])
                #print(r, ":", majority, minority, undecided)
    return majority, minority, undecided
 


def binomial(cherries, percentCherry):
    percent = combDict[str(cherries)] * (percentCherry**cherries) * (1-percentCherry)**(sampleSize-cherries)
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
    for cherries in range(0, sampleSize+1):
        percent = binomial(cherries, percentCherry)
        if cherries < sampleSize/2:
            minority += percent
        elif cherries > sampleSize/2:
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


initialPriors =    [1/3 for i in range(0, 3)]
priorsCherryProb = [.25, .5, .75]
rounds = 2
sampleSize = 10
combDict = {}
for cherries in range(0, sampleSize+1):
    comb = ncr(sampleSize, cherries)
    combDict[str(cherries)] = comb
updatedPriorsDict = {}
for cherries in range(0, sampleSize+1):
    init = [p for p in initialPriors]
    updatedPriorsDict[str(cherries)] = updatePriors(cherries, sampleSize-cherries, init, priorsCherryProb)


# agents stuff
observedCherries = 8
observedLimes= sampleSize-observedCherries
init = [p for p in initialPriors]
myPriors = updatePriors(observedCherries, observedLimes, init, priorsCherryProb)
majority, minority, undecided = estimates(myPriors, priorsCherryProb, 1)
probCherry = getPi(myPriors, priorsCherryProb)
print(probCherry)
print(majority, minority, undecided)
if profitable(probCherry, majority, minority):
    print("cherry profitable")
elif profitable(1-probCherry, minority, majority):
    print("lime profitable")
else:
    print("don't vote")
