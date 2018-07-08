# -*- coding: utf-8 -*-
"""
Simlate a biased coin
"""

import numpy as np

class biased_coin:
    """ biased_ is a class that implements a biased coin with
        probability of heads = p, probability of tails = 1-p """
    def __init__(self, p):
        self.p = p
      
    def toss(self):
        """ generate a single toss of the biased coin """  
        if np.random.rand() > self.p:
            return 'T'
        else:
            return 'H'

    def get_sequence(self,num_tosses):
        
        seq = [self.toss() for i in range(num_tosses)]
        return seq
        
        
def main():
    p = 0.7 # probability of heads
    c = biased_coin(0.7);
    tosses = c.get_sequence(100);
    num_heads = tosses.count('H')
    num_tails = tosses.count('T')
    print ("simulated 100 tosses of a biased coin with p = " + str(p))
    print ("obtained " + str(num_heads) + " heads and " + str(num_tails) + " tails")



if __name__ == '__main__':
    main()