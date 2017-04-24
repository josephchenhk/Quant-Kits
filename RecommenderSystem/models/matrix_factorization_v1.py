# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:31:44 2017

@author: joseph.chen

An implementation of matrix factorization

Ref: http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

"""

import numpy as np
import copy
import random

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
                    
        if e < 0.01:
            break
    
#    print("Number of iteration:",step+1)
#    print("Precision:",e)
            
    return P, Q.T
#
#def matrix_factorization2(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
#    QT = Q.T
#    PT = P.T
#
#    for step in range(steps):
#        e = 0
#        N = 0
#        for i in range(len(R)):
#            for j in range(len(R[i])):
#                if R[i][j] > 0:
#                    N += 1.0
#                    eij = R[i][j] - np.dot(P[i,:],QT[:,j])
#                    e = e + pow(eij,2)
#                    for k in range(K):
#                        RQ = np.dot(R,Q)
#                        PQTQ = np.dot(np.dot(P,QT),Q)
#                        P[i][k] = P[i][k]*RQ[i][k]/PQTQ[i][k]
#                        
#                        PT = P.T
#                        PTR = np.dot(PT,R)
#                        PTPQT = np.dot(np.dot(PT,P),QT)
#                        QT[k][j] = QT[k][j]*PTR[k][j]/PTPQT[k][j]
#                        Q = QT.T
#        
#                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(QT[k][j],2) )
#
#
#
#        e = np.sqrt(e/N)    
#        #print(e)            
#        if e < 0.01:
#            break
#    
#    print("Number of iteration:",step+1)
#    print("Precision:",e)
##            
#    return P, Q

def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

def betting(R,k):
    num_question = len(R[k])
    bet = np.zeros(R.shape) 
    for n in range(75):
        num_question_candidate = random.choice(range(num_question)) + 1
        questions = random.sample(range(num_question),num_question_candidate)
        prob = []
        for q in questions:
            prob.append(R[k][q])
        if sum(prob)!=0:
            prob = [p/sum(prob) for p in prob]
        else:
            prob = [1./len(prob) for p in prob]
        question = random_pick(questions, prob)
        bet[k][question] += 1    
    return bet

def RR2R(RR,max_rating,min_rating): # Raw R to R
    N,M = RR.shape
    max_raw = np.amax(RR)
    R = copy.deepcopy(RR)
    for n in range(N):
        for m in range(M):
            R[n][m] = RR[n][m]*max_rating/max_raw
    R = np.maximum(R,min_rating)
    return R

def R2RR(R,total_wager):  # R to Raw R
    N,M = R.shape
    total_rating = sum(sum(R))
    RR = copy.deepcopy(R)
    for n in range(N):
        for m in range(M):
            RR[n][m] = R[n][m]*total_wager/total_rating
    return RR
 


def updateRR(RR, bet):
    return RR+bet

###############################################################################

if __name__ == "__main__":
    
    num_room = 5
    num_question = 4
    max_rating = 5
    min_rating = 0
    init_wager = 1000.  # assume initial 
    
#    R = [
#         [5,3,0,1],
#         [4,0,0,1],
#         [1,1,0,5],
#         [1,0,0,4],
#         [0,1,5,4],
#        ]
#    R = np.array(R)

#    R = [[ 3.,  0.,  0.,  0.],
#         [ 2.,  2.,  4.,  2.],
#         [ 1.,  5.,  3.,  5.],
#         [ 5.,  3.,  0.,  3.],
#         [ 4.,  0.,  1.,  1.]]
#    R = np.array(R)

    # R: rating matrix with maximum rating
    R = np.zeros((num_room, num_question)) 
    for n in range(num_room):
        for m in range(num_question):
            R[n][m] = random.sample(range(max_rating+1),1)[0]
    print(R)  
    
    # raw R: dollar matrix that represents the popularity of questions
    RR = R2RR(R,init_wager)
    #print(RR)
    

    N = len(R)
    M = len(R[0])
    K = 2

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = np.dot(nP, nQ.T)
    nR = RR2R(nR,max_rating,min_rating)
    
    print("\nStart")
    for n in range(3): # number of update
        for k in range(len(nR)): # match (chatroom)
            bet = betting(nR,k)
            RR = updateRR(RR,bet)
            R = RR2R(RR,max_rating,min_rating)
            nP, nQ = matrix_factorization(R, P, Q, K)
            nR = np.dot(nP, nQ.T)
            nR = RR2R(nR,max_rating,min_rating)
        print(R)
        print("\n")
        