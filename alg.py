import operator as op
from functools import reduce
import math
import copy
import sys


round_decimal_place = 6
combinations_dict = None

CHERRY = "CHERRY"
LIME = "LIME"
ABSTAIN = "ABSTAIN"


class Hypothesis:
    
    def __init__(self, cherry, lime, prob):
        assert(cherry + lime == 1)
        self.prob = prob
        self.cherry = cherry
        self.lime = lime


    def __str__(self):
        return "(cherry: " + str(round(self.cherry,2)) + ", lime: " + str(round(self.lime, 2)) + " --> " + str(round(self.prob,2)) + ")"

# uses global combinationsDict object to make calculations faster
def binomial(cherries, limes, percent_cherry, percent_lime):
    percent = combinations_dict[str(cherries)] * (percent_cherry**cherries) * (percent_lime)**(limes)
    return percent


# TODO: this might be wrong 
def update_priors(observations, sample_size, initial_priors):
    num_cherry = observations[0] 
    num_lime = observations[1] 
    assert(num_cherry + num_lime == sample_size)

    priors = copy.deepcopy(initial_priors)
    for c in range(0, num_cherry):
        priors_unscaled = []
        for j in range(0, len(priors)):
            Hi = priors[j]
            P_Ci = Hi.cherry
            P_Li = Hi.lime
            P_Hi = Hi.prob
            priors_unscaled += [P_Ci * P_Hi]
        s = sum(priors_unscaled)
        for j in range(0, len(priors)):
            priors[j].prob = priors_unscaled[j] / s

    for i in range(0, num_lime):
        priors_unscaled = []
        for j in range(0, len(priors)):
            Hi = priors[j]
            P_Ci = Hi.cherry
            P_Li = Hi.lime
            P_Hi = Hi.prob
            priors_unscaled += [P_Li * P_Hi]
        s = sum(priors_unscaled)
        for j in range(0, len(priors)):
            priors[j].prob = priors_unscaled[j] / s

    return priors


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


def make_combinations_dict(sampleSize):
    comb_dict = {}
    for cherries in range(0, sampleSize+1):
        comb = ncr(sampleSize, cherries)
        comb_dict[str(cherries)] = comb
    return comb_dict



def imperfect_info_algo(observations, sample_size, initial_priors, R, r=0):
    priors = update_priors(observations, sample_size, initial_priors)
    P_C = P_L = 0 

    if r == R: # base case
        M_C = 0
        M_L = 0
        for h in priors:
            P_Hi = h.prob
            P_Ci = h.cherry
            P_Li = h.lime
            if P_Ci > P_Li:
                M_C += P_Hi
            elif P_Li > P_Ci:
                M_L += P_Hi
        M_L = round(M_L, round_decimal_place)
        M_C = round(M_C, round_decimal_place)
        #print("M_L", M_L, "M_C", M_C)
        if M_C > M_L: this_vote = "cherry"
        elif M_L > M_C: this_vote = "lime"
        else: this_vote = "abstain" 
        return this_vote
    else:
        cherry_sum = lime_sum = 0
        cherry_revenue = lime_revenue = 0
        cherry_cost = lime_cost = 0
        cherry_profit = lime_profit = 0
        for h in priors:
            P_Hi = h.prob
            P_Ci = h.cherry
            P_Li = h.lime
            for next_cherries in range(0, sample_size+1):
                next_limes = sample_size - next_cherries
                next_observations = (next_cherries, next_limes)
                next_vote = imperfect_info_algo(next_observations, sample_size, initial_priors, R, r+1)
                binomial_prob = binomial(next_cherries, next_limes, P_Ci, P_Li)
                normalized_binomial_prob = binomial_prob * P_Hi 
                if next_vote == "cherry": cherry_sum += normalized_binomial_prob
                elif next_vote == "lime": lime_sum += normalized_binomial_prob
                elif next_vote == "abstain": pass
            if cherry_sum > lime_sum:
                cherry_revenue += P_Hi * (lime_sum/cherry_sum)
                lime_cost += P_Hi
            elif lime_sum > cherry_sum:
                lime_revenue += P_Hi * (cherry_sum/lime_sum)
                cherry_cost += P_Hi
            cherry_profit = cherry_revenue - cherry_cost
            lime_profit = lime_revenue - lime_cost
            if cherry_profit > lime_profit and cherry_profit > 0: this_vote = "cherry"
            elif lime_profit > lime_profit and lime_profit > 0: this_vote = "lime"
            else: this_vote = "abstain"
            return this_vote
                

def make_hypothesis_list(priors_probs, priors_cherry_probs):
    initial_priors = []
    for i in range(0, len(priors_probs)):
        P_Ci = priors_cherry_probs[i]
        P_Li = 1-P_Ci
        prob = priors_probs[i]
        initial_priors += [Hypothesis(P_Ci, P_Li, prob)]
    return initial_priors 


def experimentHeaderPrint(observations, sample_size, initial_priors, R):
    print("number of recursive rounds:", R)
    print("sample size:", sample_size)
    print("initial priors mapping:")
    for prior in initial_priors:
        print(prior)
    print("my observations: cherries:", observations[0], "limes:", observations[1])
    #print("decision weight:", decisionWeight)


def main():
    global combinations_dict 
    if len(sys.argv) == 1:
        R = 3 # default recusive is 3
    else:
        R = int(sys.argv[1])

    sample_size = 10
    combinations_dict = make_combinations_dict(sample_size)
    priors_probs = [1/5 for i in range(0, 5)]
    priors_cherry_probs = [0, .25, .5, .75, 1]
    initial_priors = make_hypothesis_list(priors_probs, priors_cherry_probs)

    # we don't need to do the other half because
    # it is should have a mirror and flipped result to the first half,
    # hence the sample_size//2 + 2
    #for cherries in range(0, (sample_size//2)+2):
    for cherries in range(0, sample_size+1):
        limes = sample_size - cherries
        observations = (cherries,limes)
        experimentHeaderPrint(observations, sample_size, initial_priors, R)
        vote = imperfect_info_algo(observations, sample_size, initial_priors, R)
        print(vote)
        print()



main()


def old_main():
    global combinations_dict 
    rounds = 3
    sample_size = 20
    combinations_dict = makeCombDict(sample_size)
    observedCherries = 16
    initialPriors =    [1/5 for i in range(0, 5)]
    priorsCherryProb = [0, .2, .6, .8, 1]
    decisionWeight = 0
    experimentHeaderPrint(rounds, sampleSize, initialPriors, priorsCherryProb, observedCherries, decisionWeight)
    count = 0
    for cherries in range(0, sampleSize+1):
        print(cherries, "observed cherries")
        cherryChoiceProfit, limeChoiceProfit, choice = decide(cherries, sampleSize, rounds, initialPriors, priorsCherryProb, decisionWeight)
        if choice != undecidedStr:
            print(cherries, "is profitable:", cherryChoiceProfit, limeChoiceProfit)
            count += 1
        else:
            print("not profitable")
    if count == 0: 
        print("none are profitable")

