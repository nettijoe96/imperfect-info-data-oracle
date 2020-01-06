from matplotlib import pyplot as plt
import bayes
from itertools import combinations

m = 30
n = 8
pi = .5

priorsCherryProb100 = [1/100 * i for i in range(0, 101)]    #percent of cherrys from 0% to 100%
priors100 = [1/len(priorsCherryProb100) for i in range(0, len(priorsCherryProb100))] #equal starting priors

def main():
    priorsCherryProb = priorsCherryProb100
    initalPriors = [p for p in priors100]
    data = generateData(priorsCherryProb)
    piCountDict = {}
    totalMatches = 0
    combProb = {}
    for i in range(0, len(priorsCherryProb)):
        print("prior ", i, "is true")
        count = 0
        combs = getCombinations(data[i])
        for comb in combs:
            combKey = getCombKey(comb)
            if combKey in combProb:
                prob = combProb[combKey]
            else: 
                priors = [p for p in initalPriors]
                prob = round(getPi(comb, priors, priorsCherryProb),1)
                combProb[combKey] = prob
                print(prob)
            if prob == pi:              # TODO: maybe we should check within a range
                totalMatches += 1 
                count += 1
        key = str(priorsCherryProb[i])
        piCountDict[key] = count
        combs = None
         
    graphPiCount(priorsCherryProb, piCountDict, totalMatches)
 

def getCombKey(comb):
    cherry = 0
    lime = 0
    for ele in comb:
        if ele == "cherry":
            cherry += 1
        else:
            lime += 1
    return str((cherry, lime))


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


def getCombinations(data):
    return list(combinations(data, n))


def getPi(data, initalPriors, priorsCherryProb):
    priors = initalPriors
    for i in range(0, len(data)):
        d = data[i]
        priorsUnscaled = []
        if d == "cherry":
             for j in range(0, len(priors)):
                priorsUnscaled += [priorsCherryProb[j] * priors[j]]
        else:
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


