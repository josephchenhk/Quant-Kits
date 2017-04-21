# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:02:16 2017

@author: joseph.chen

Ref: http://stackoverflow.com/questions/22767695/python-non-negative-matrix-factorization-that-handles-both-zeros-and-missing-dat
"""

import numpy as np
from scipy import linalg
from numpy import dot

def nmf(X, latent_features, max_iter=1000, error_limit=1e-6, fit_error_limit=1e-6):
    """
    Decompose X to A*Y
    """
    eps = 1e-5
    print('Starting NMF decomposition with {} latent features and {} iterations.'.format(latent_features, max_iter))
    #X = X.toarray()  # I am passing in a scipy sparse matrix

    # mask
    mask = np.sign(X)

    # initial matrices. A is random [0,1] and Y is A\X.
    rows, columns = X.shape
    A = np.random.rand(rows, latent_features)
    A = np.maximum(A, eps)

    Y = linalg.lstsq(A, X)[0]
    Y = np.maximum(Y, eps)

    masked_X = mask * X
    X_est_prev = dot(A, Y)
    for i in range(1, max_iter + 1):
        # ===== updates =====
        # Matlab: A=A.*(((W.*X)*Y')./((W.*(A*Y))*Y'));
        top = dot(masked_X, Y.T)
        bottom = (dot((mask * dot(A, Y)), Y.T)) + eps
        A *= top / bottom

        A = np.maximum(A, eps)
        # print 'A',  np.round(A, 2)

        # Matlab: Y=Y.*((A'*(W.*X))./(A'*(W.*(A*Y))));
        top = dot(A.T, masked_X)
        bottom = dot(A.T, mask * dot(A, Y)) + eps
        Y *= top / bottom
        Y = np.maximum(Y, eps)
        # print 'Y', np.round(Y, 2)


        # ==== evaluation ====
        if i % 5 == 0 or i == 1 or i == max_iter:
            print('Iteration {}:'.format(i))
            X_est = dot(A, Y)
            err = mask * (X_est_prev - X_est)
            fit_residual = np.sqrt(np.sum(err ** 2))
            X_est_prev = X_est

            curRes = linalg.norm(mask * (X - X_est), ord='fro')
            print('fit residual', np.round(fit_residual, 4))
            print('total residual', np.round(curRes, 4))
            if curRes < error_limit or fit_residual < fit_error_limit:
                break

    return A, Y


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
    
    W, H = nmf(R, 2)
    
    print(W.dot(H))