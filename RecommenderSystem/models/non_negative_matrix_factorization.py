# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:43:46 2017

@author: joseph.chen
"""

import numpy as np

def update(V, W, H, r, n, m):
    n,m = V.shape 
    WH = W.dot(H)

    # equation (5)
    H_coeff = np.zeros(H.shape)
    for a in range(r):
        for mu in range(m):
            for i in range(n):
                H_coeff[a, mu] += W[i, a] * V[i, mu] / WH[i, mu]
            H_coeff[a, mu] /= sum(W)[a]
    H = H * H_coeff
    
    # Before update W, need to update WH first
    WH = W.dot(H)

    W_coeff = np.zeros(W.shape)
    for i in range(n):
        for a in range(r):
            for mu in range(m):
                W_coeff[i, a] += H[a, mu] * V[i, mu] / WH[i, mu]
            W_coeff[i, a] /= sum(H.T)[a]
    W = W * W_coeff

    return W, H


def factor(V, r, iterations=100):
    n, m = V.shape
    avg_V = sum(sum(V))/n/m
    W = np.random.random(n*r).reshape(n,r)*avg_V
    H = np.random.random(r*m).reshape(r,m)*avg_V

    for i in range(iterations):
        WH = W.dot(H)
        #divergence = sum(sum(V * np.log(V/WH) - V + WH)) # equation (3)
        divergence = sum(sum(pow(V - WH,2)))  # equation (2)
        print("At iteration " + str(i) + ", the Kullback-Liebler divergence is", divergence)
        W,H = update(V, W, H, r, n, m)

    return W, H


if __name__=="__main__":
    #V = np.arange(0.01,1.01,0.01).reshape(10,10)
    
    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ]
    
    # This method requires that elements in R matrix must be positive
#    R = [
#         [5,3,2,1],
#         [4,2,2,1],
#         [1,1,2,5],
#         [1,2,2,4],
#         [2,1,5,4],
#        ]

    R = np.array(R)
    
    W, H = factor(R, 6)
    
    print(W.dot(H))