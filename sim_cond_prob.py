# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 22:24:01 2018

@author: santhosh

-mcmm-

simple examples showing the use of monte carlo methods:
1. to generate samples from p(y), given p(y|x) and p(x)
2. to generate samples from a "posterior", p(x|y), given "likelihood", p(y|x)
   and "prior" p(x)
"""
import numpy as np
import matplotlib.pyplot as plt

def findx(c,r):
    """
    Returns the smallest index of the element(s) in c that is nearest to r

    Keyword arguements:
    c: cumulative sum of a probability function
    r: a value between 0.0 and 1.0
    """
    idxs = np.zeros(len(r), dtype=int)
    for i in range(len(r)):
        idxs[i] = int(np.argmin(c < r[i]))

    return idxs

def sample(labels, p, N):
    """
    samples random variables according to a given probability mass function

    Keyword arguments:
    labels: the values that the random variables can take (e.g. [0,1] or ['H','T'])
    p: probability mass function (p[i] >= 0 and p.sum() == 1.0)
    N: The number of samples

    Returns an array of random variables
    """
    c = p.cumsum()
    r = np.random.uniform(0,1,N)
    idxs = findx(c,r)
    x = labels[idxs]
    return x


if __name__ == '__main__':
    y_labels = np.array([0,1])
    x_labels = np.array([0,1])

    """
       p_x = p(x)
       p(x == 0) = 0.6 and p(x == 1) = 0.4
    """

    p_x = np.array([0.6,0.4])

    """
       p_y_x = p(y|x)
       p(y|x = 0) = 0.1, y == 0
                  = 0.9, y == 1

       p(y|x = 1) = 0.7, y == 0
                  = 0.3, y == 1
    """

    p_y_x = np.array([[0.1,0.9],[0.7,0.3]])

    """
    Task 1: We wish to determine p(y)
            By the "law of total probability", we have
            p(y == 0) = 0.1 * 0.6 + 0.7 * 0.4 = 0.34
            p(y == 1) = (1 - 0.34) = 0.66

            For doing this the "Monte Carlo" way, we first
            simulate a bunch of 'x's according to p(x)
            and for each x, we simulate a bunch of 'y's according
            to p(y|x). Finally, a histogram should give us the
            desired answer
    """
    x = sample(x_labels, p_x, 10000)
    y = np.array([])
    for i in range(len(x)):
        q = p_y_x[x[i],]
        y = np.append(y, sample(y_labels, q, 10))

    cnt_y = np.array([(y == 0).sum(), (y == 1).sum()])
    p_y = cnt_y/len(y)
    print('p(y) is: [%1.2f, %1.2f]'%(p_y[0], p_y[1]))

    """
    Task 2: Sample from posterior. We wish to determine
            p(x|y); say, p(x == 0 | y = 0), p(x == 1| y = 0)
            This is easily done by applying Bayes' theorem
            p(x|y) = p(y|x) p(x) / sum_x (p(y|x) p(x))
            e.g.:
            p(x == 0| y = 0) = p(y == 0| x = 0) p(x == 0)
                              ----------------------------
              (p(y == 0| x = 0) p(x == 0) + p(y == 0| x = 1) p(x == 1))

              = 0.1 * 0.6 / (0.1 * 0.6 + 0.7 * 0.4) = 0.06 / 0.34 = 0.176

             and,
             p(x == 1| y = 0) = (1 - 0.176) = 0.823

             similarly,
             p(x == 0| y = 1) = 0.9 * 0.6/(0.9 * 0.6 + 0.3 * 0.4) = 0.818
             and
             p(x == 1| y = 1) = (1 - 0.818) = 0.182

             ---------

             To do this the "Monte Carlo" way, we begin by sampling
             x from p(x). Then, for each x, we generate a y based on
             p(y|x).
             Now, choose only those x:s from which y = 1 was generated and
             discard the rest. The new set of x's (the resampled batch)
             would have the distribution p(x|y=1)
    """
    x = sample(x_labels, p_x, 10000)
    x_new = np.array([])
    for i in range(len(x)):
        q = p_y_x[x[i],]
        y = sample(y_labels, q, 1)
        if y == 0:
            x_new = np.append(x_new, x[i])

    #done! now, check the distribution
    cnt_x_new = np.array([(x_new == 0).sum(), (x_new == 1).sum()])
    p_x_y0 = cnt_x_new / len(x_new)
    print('p(x|y=0) is: [%1.2f, %1.2f]'%(p_x_y0[0], p_x_y0[1]))
    print('INFO: len(x) = %d, len(x_new) = %d'%(len(x), len(x_new)))



