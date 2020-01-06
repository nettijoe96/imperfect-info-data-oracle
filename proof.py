from matplotlib import pyplot as plt
import bayes
from itertools import combinations
import operator as op
from functools import reduce


m = 1000
n = 30
pi = .78

priorsCherryProb100 = [1/100 * i for i in range(0, 101)]    #percent of cherrys from 0% to 100%
priors100 = [1/len(priorsCherryProb100) for i in range(0, len(priorsCherryProb100))] #equal starting priors

def main():
    priorsCherryProb = priorsCherryProb100
    initalPriors = [p for p in priors100]
    data = generateData(priorsCherryProb)
    piCountDict = {}
    totalMatches = 0
    combProb = {}
    numOfCherriesNeeded = None
    for i in range(0, n+1):   #number of cherry's to get prob
        priors = [p for p in initalPriors]
        prob = round(getPi(i, n-i, priors, priorsCherryProb), 2)
        print(prob)
        if prob == pi:
            numOfCherriesNeeded = i
            break
    if numOfCherriesNeeded is None:
        print("choose different pi")
        return

    for i in range(0, len(priorsCherryProb)):
        print("prior ", i, "is true")
        count = 0
        ds = data[i]
        cherry = 0
        lime = 0
        for d in ds:
            if d == "cherry":
                cherry += 1
            else:
                lime += 1
        percentCherry = cherry/len(ds)
        percentLime = lime/len(ds)
        
        #prob of getting number of cherries needed
        combNum = ncr(m, n)
        binomial = round(combNum * (percentCherry**numOfCherriesNeeded) * (percentLime**(n-numOfCherriesNeeded)))
        piCountDict[str(priorsCherryProb[i])] = binomial
        totalMatches += binomial 

    graphPiCount(priorsCherryProb, piCountDict, totalMatches)
 

def ncr(a, b):
    r = min(b, a-b)
    numer = reduce(op.mul, range(a, a-b, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


def graphPiCount(priorsCherryProb, piCountDict, totalMatches):
    x = priorsCherryProb
    y = [piCountDict[str(priorsCherryProb[i])] / totalMatches for i in range(0, len(priorsCherryProb))]
    plt.plot(x,y) 
    plt.show()

def generateData(priorsCherryProb):
    data = []
    for i in range(0, len(priorsCherryProb)):
        cherryProb = priorsCherryProb[i]
        data += [bayes.generate(cherryProb, m)]
    return data


def getPi(cherries, limes, initalPriors, priorsCherryProb):
    priors = initalPriors
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
 
    prob = 0
    for j in range(0, len(priors)):
        prob += priorsCherryProb[j] * priors[j]

    return prob


main()


