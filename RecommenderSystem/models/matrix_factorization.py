#!/usr/bin/python
#
# Created by Joseph Chen
#
# An implementation of matrix factorization
#
# Ref: http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/
import numpy as np

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
#def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
#    Q = Q.T
#    for step in range(steps):
#        for i in range(len(R)):
#            for j in range(len(R[i])):
#                if R[i][j] > 0:
#                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
#                    for k in range(K):
#                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
#                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
#        eR = np.dot(P,Q)
#        e = 0
#        for i in range(len(R)):
#            for j in range(len(R[i])):
#                if R[i][j] > 0:
#                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
#                    for k in range(K):
#                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
#        if e < 0.001:
#            break
#    return P, Q.T

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        e = 0
        N = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    N += 1.0
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    e = e + pow(eij,2)
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        e = np.sqrt(e/N)    
                    
        print(e)
        if e < 0.01:
            break
    
    print("Number of iteration:",step+1)
    print("Precision:",e)
            
    return P, Q.T

###############################################################################

if __name__ == "__main__":
    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ]

    R = np.array(R)

    N = len(R)
    M = len(R[0])
    K = 2

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = np.dot(nP, nQ.T)
    print(nR)
