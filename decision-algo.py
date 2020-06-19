import operator as op
from functools import reduce
import math
import copy
import sys


combinations_dict = None
CHERRY = "CHERRY"
LIME = "LIME"
ABSTAIN = "ABSTAIN"
ROUND_DECIMAL_PLACE = 6


class Hypothesis:
    """
    A hypothesis of the distribution of candies in the bag. 
    There are two types of candies so cherry + lime probabilities must equal 1
    The hypothesis has some prior probability of being correct
    """
    
    def __init__(self, cherry, lime, prob):
        assert(cherry + lime == 1)
        self.prob = prob
        self.cherry = cherry
        self.lime = lime

    def __str__(self):
        return "(cherry: " + str(round(self.cherry,2)) + ", lime: " + str(round(self.lime, 2)) + " --> " + str(round(self.prob,2)) + ")"


def binomial(A_num, B_num, A_prob, B_prob):
    """
    binomial distribution formula
    uses global combinations_dict object to make calculations faster
    @param A_num: number of A obsevations
    @param B_num: number of B observations
    @param A_prob: probability of observing A
    @param B_prob: probabliity of observing B
    @return probability    
    """
    probability = combinations_dict[str(A_num)] * float(A_prob**A_num) * float(B_prob**B_num)
    return probability


def update_priors_batch(observations, sample_size, initial_priors):
    """
    updates priors with observations
    assertion: sum of observations tuple must be the sample_size.
    @param observations: tuple of observations (#cherry, #lime)
    @param sample_size
    @param initial_priors: list of hypothesis objects whose probs must add to 1
    @return posteriers
    """
    num_cherry = observations[0]
    num_lime = observations[1]
    assert(num_cherry + num_lime == sample_size)
    priors = copy.deepcopy(initial_priors)

    denom = 0
    nums = []
    for i in range(0, len(priors)):
        Hi = priors[i]
        P_Ci = Hi.cherry
        P_Li = Hi.lime
        P_D = binomial(num_cherry, num_lime, P_Ci, P_Li) * Hi.prob
        nums += [P_D]
        denom += P_D
    for i in range(0, len(priors)):
        num = nums[i]
        priors[i].prob = num/denom

    for p in priors:
        p.prob = round(p.prob, ROUND_DECIMAL_PLACE)

    return priors


def ncr(n, r):
    """
    number of combinations function
    n choose r
    @param n
    @param r
    @param # of combinations
    """
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


def make_combinations_dict(sample_size):
    """
    for speeding up computation, we create a dict mapping r (in n choose r) to number of combinations
    @param sample_size
    @return combination dict
    """
    comb_dict = {}
    for cherries in range(0, sample_size+1):
        comb = ncr(sample_size, cherries)
        comb_dict[str(cherries)] = comb
    return comb_dict


def compare_priors(priors1, priors2):
    for i in range(0, len(priors1)):
        p1i = priors1[i] 
        p2i = priors2[i] 
        if p1i.prob != p2i.prob:
            return False
    return True


def print_priors(priors):
    """
    print the priors
    @param priors
    """
    for p in priors:
        print(p)


def imperfect_info_decision_algo(observations, sample_size, initial_priors, R, r=0):
    """
    The most important function of this repository
    It is the imperfect information decision algorithm
    See paper for explanation of the algorithm.
    @param observations: tuple of observations (#cherry, #lime)
    @param sample_size
    @param initial_priors: list of hypothesis objects whose probs must add to 1
    @param R: number of recursive rounds
    @param r: current recursive round
    @return: vote
    """
    priors = update_priors_batch(observations, sample_size, initial_priors)

    if r == R:  # base case
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
        M_L = round(M_L, ROUND_DECIMAL_PLACE)
        M_C = round(M_C, ROUND_DECIMAL_PLACE)
        if M_C > M_L: this_vote = "cherry"
        elif M_L > M_C: this_vote = "lime"
        else: this_vote = "abstain" 
        return this_vote
    else:
        cherry_revenue = 0
        lime_revenue = 0
        cherry_cost = 0
        lime_cost = 0
        for i in range(len(priors)):
            h = priors[i]
            cherry_proportion = 0
            lime_proportion = 0
            P_Hi = h.prob
            P_Ci = h.cherry
            P_Li = h.lime
            for next_cherries in range(0, sample_size+1):
                next_limes = sample_size - next_cherries
                next_observations = (next_cherries, next_limes)
                next_vote = imperfect_info_decision_algo(next_observations, sample_size, initial_priors, R, r+1)
                binomial_prob = binomial(next_cherries, next_limes, P_Ci, P_Li)
                if next_vote == "cherry": cherry_proportion += binomial_prob
                elif next_vote == "lime": lime_proportion += binomial_prob
                elif next_vote == "abstain": pass
            cherry_proportion = round(cherry_proportion, ROUND_DECIMAL_PLACE)
            lime_proportion = round(lime_proportion, ROUND_DECIMAL_PLACE)
            if cherry_proportion > lime_proportion:
                delta_rev = P_Hi * (lime_proportion/cherry_proportion)
                cherry_revenue += delta_rev
                lime_cost += P_Hi
            elif lime_proportion > cherry_proportion:
                delta_rev = P_Hi * (cherry_proportion/lime_proportion)
                lime_revenue += delta_rev
                cherry_cost += P_Hi
        cherry_profit = cherry_revenue - cherry_cost
        lime_profit = lime_revenue - lime_cost
        if cherry_profit > lime_profit and cherry_profit > 0: this_vote = "cherry"
        elif lime_profit > cherry_profit and lime_profit > 0: this_vote = "lime"
        else: this_vote = "abstain"
        return this_vote
                

def make_hypothesis_list(priors_probs, priors_cherry_probs):
    """
    @param priors_probs: list of probabilities of a hypotheses being true
    @param priors_cherry_prob: list of distribution of cherries
    @return hypothesis list
    """
    initial_priors = []
    for i in range(0, len(priors_probs)):
        P_Ci = priors_cherry_probs[i]
        P_Li = 1-P_Ci
        prob = priors_probs[i]
        initial_priors += [Hypothesis(P_Ci, P_Li, prob)]
    return initial_priors 


def experiment_header_print(observations, sample_size, initial_priors, R):
    print("number of recursive rounds:", R)
    print("sample size:", sample_size)
    print("initial priors mapping:")
    for prior in initial_priors:
        print(prior)
    print("my observations: cherries:", observations[0], "limes:", observations[1])


def print_revenue_cost(cherry_revenue, lime_revenue, cherry_cost, lime_cost):
    print("cherry_rev", cherry_revenue, "cherry_cost", cherry_cost, "lime_rev", lime_revenue, "lime_cost", lime_cost)


def main():
    """
    command line argument dictates number of recursive rounds
    runs the decision algorithm for each observation set
    prints the result for each observation set
    """
    global combinations_dict 
    if len(sys.argv) == 1:
        R = 2 # default recusive is 2
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
        observations = (cherries, limes)
        experiment_header_print(observations, sample_size, initial_priors, R)
        vote = imperfect_info_decision_algo(observations, sample_size, initial_priors, R)
        print(vote)
        print()

main()

