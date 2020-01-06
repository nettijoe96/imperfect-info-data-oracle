"""
a small example of prior updating and bayesian prediction 

question 20.1 in artificial intelligence: a modern approach by Russell and Norvig 3rd edition

Joe Netti
"""

from matplotlib import pyplot as plt
import pandas as pd
import random 

priors = [.1, .2, .4, .2, .1]
ext = ".txt"
roundNum = 100  #100 data pieces drawn

def main():
    h1 = 1
    p1, p2, p3, p4, p5 = probDist(generate(h1, roundNum))
    plime = predictNextLime(p1, p2, p3, p4, p5)
    graph(h1, plime, p1, p2, p3, p4, p5)
    h2 = .75
    p1, p2, p3, p4, p5 = probDist(generate(h2, roundNum))
    plime = predictNextLime(p1, p2, p3, p4, p5)
    graph(h2, plime, p1, p2, p3, p4, p5)
    h3 = .5
    p1, p2, p3, p4, p5 = probDist(generate(h3, roundNum))
    plime = predictNextLime(p1, p2, p3, p4, p5)
    graph(h3, plime, p1, p2, p3, p4, p5)
    h4 = .25
    p1, p2, p3, p4, p5 = probDist(generate(h4, roundNum))
    plime = predictNextLime(p1, p2, p3, p4, p5)
    graph(h4, plime, p1, p2, p3, p4, p5)


"""
generates data according to the hypothesis type
@param: hypothesis type
@return: data list
"""
def generate(cherryProb, roundNum):
    data = []
    for i in range(0, roundNum):
        r = random.random()
        if r < cherryProb:
            data += ["cherry"]
        else:
            data += ["lime"]

    return data

"""
the probability of the hypothesises being true after bayes is updated from a data piece
@param: data list
@return: the list of probabilities
"""
def probDist(data):
    p1 = [priors[0]]
    p2 = [priors[1]]
    p3 = [priors[2]]
    p4 = [priors[3]]
    p5 = [priors[4]]
    for i in range(0, roundNum):
        d = data[i]
        if d == "cherry":
            p1Unscaled = 1*p1[i]
            p2Unscaled = .75*p2[i]
            p3Unscaled = .5*p3[i]
            p4Unscaled = .25*p4[i]
            p5Unscaled = 0*p5[i]
            s = p1Unscaled + p2Unscaled + p3Unscaled + p4Unscaled + p5Unscaled 
            p1 += [p1Unscaled/s]
            p2 += [p2Unscaled/s]
            p3 += [p3Unscaled/s]
            p4 += [p4Unscaled/s]
            p5 += [p5Unscaled/s]
        else:
            p1Unscaled = 0*p1[i]
            p2Unscaled = .25*p2[i]
            p3Unscaled = .5*p3[i]
            p4Unscaled = .75*p4[i]
            p5Unscaled = 1*p5[i]
            s = p1Unscaled + p2Unscaled + p3Unscaled + p4Unscaled + p5Unscaled 
            p1 += [p1Unscaled/s]
            p2 += [p2Unscaled/s]
            p3 += [p3Unscaled/s]
            p4 += [p4Unscaled/s]
            p5 += [p5Unscaled/s]
  
    return p1, p2, p3, p4, p5


"""
used if you want to load data from a file
@param: filename
@param: data list
"""
def loadDataFromFile(dataFileName):
    f = open(dataFileName, "r")
    data = []
    for i in range(0, 100):
        data += [f.readline().strip("\n")] 
    return data 


"""
determining whether the next candy is a cherry or lime
@param p1: prob list for hypothesis 1
@param p2: prob list for hypothesis 2
@param p3: prob list for hypothesis 3
@param p4: prob list for hypothesis 4
@param p5: prob list for hypothesis 5
@return: plst
"""
def predictNextLime(p1, p2, p3, p4, p5):
   plst = []
   for i in range(0, 101):
       p = 0
       p += 0*p1[i]
       p += .25*p2[i]
       p += .5*p3[i]
       p += .75*p4[i]
       p += 1*p5[i]
       plst += [p]
   return plst



"""
make 2 graphs. One for the probabilities of hypothesis being true over time.
The other for the probability the next is a lime
@param: title
@param plime: probability list that the next is lime at any point in time
@param p1: prob list for hypothesis 1
@param p2: prob list for hypothesis 2
@param p3: prob list for hypothesis 3
@param p4: prob list for hypothesis 4
@param p5: prob list for hypothesis 5
"""
def graph(title, plime, p1, p2, p3, p4, p5):
    x = range(0, 101)
    plt.plot( x, p1, marker='o', markerfacecolor='red', markersize=6, color='red', linewidth=2, label="h1")
    plt.plot( x, p2, marker='o', markerfacecolor='orange', markersize=6, color='orange', linewidth=2,label="h2")
    plt.plot( x, p3, marker='o', markerfacecolor='blue', markersize=6, color='blue', linewidth=2, label="h3")
    plt.plot( x, p4, marker='o', markerfacecolor='purple', markersize=6, color='purple', linewidth=2, label="h4")
    plt.plot( x, p5, marker='o', markerfacecolor='green', markersize=6, color='green', linewidth=2, label="h5")
    plt.title("Prior Updating. Underlying Distribution=" + str(title))
    plt.legend()
    plt.show()
    plt.plot( x, plime, marker='o', markerfacecolor='green', markersize=6, color='green', linewidth=2, label="h5")
    plt.title("Prediction next is lime. Underlying Distribution=" + str(title))
    plt.show()


if __name__ == "__main__":
    main()

