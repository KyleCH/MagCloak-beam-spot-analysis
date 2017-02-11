#!/usr/bin/env python3

import numpy as np

# ======================================================================
# Statistical moments functions' output keys (ordered).
# ======================================================================

moment_keys = [
    'sum of weights',
    'mean',
    'variance',
    'standard deviation',
#    'skew',
#    'kurtosis',
#    'excess kurtosis',
    ]

# ======================================================================
# One-dimensional statistical moments.
# ======================================================================

def moments_1d(pos, w):
#    m = np.zeros(5)
    m = np.zeros(3)
    for n in range(pos.size):
        z = w[n]
        m[0] += z
        z *= pos[n]
        m[1] += z
        z *= pos[n]
        m[2] += z
#        z *= pos[n]
#        m[3] += z
#        z *= pos[n]
#        m[4] += z
    m[1:] /= m[0]
#    m[4] -= m[1]*(-4*m[3] + 3*m[1]*(2*m[2] - m[1]**2))
#    m[3] += m[1]*(-3*m[2] + 2*m[1]**2)
    m[2] -= m[1]**2
    s = np.sqrt(m[2])
#    m[3] /= m[2]*s
#    m[4] /= m[2]**2
    return {
        'sum of weights' : m[0],
        'mean' : m[1],
        'variance' : m[2],
        'standard deviation' : s,
#        'skew' : m[3],
#        'kurtosis' : m[4],
#        'excess kurtosis' : m[4]-3.,
        }

# ======================================================================
# Two-dimensional statistical moments.
# ======================================================================

def moments_2d(weights, pos=None):
    W = 0.
    mu1 = np.zeros(2)
    mu2 = np.zeros(2)
#    mu3 = np.zeros(2)
#    mu4 = np.zeros(2)
    if (weights.ndim == 2):
        M, N = weights.shape
    else:
        M, N = weights.shape[1:3]
    z = np.empty(2)
    if (pos is None):
        for m in range(M):
#            print('{}/{} ({:%})'.format(m, M, m/M))
            for n in range(N):
                W += weights[m, n]
                z[:] = weights[m, n]
                z *= [n, m]
                mu1 += z
                z *= [n, m]
                mu2 += z
#                z *= [n, m]
#                mu3 += z
#                z *= [n, m]
#                mu4 += z
    else:
        # If pos is formatted as an ogrid.
        if isinstance(pos, list):
            for m in range(M):
                for n in range(N):
                    W += weights[m, n]
                    z[:] = weights[m, n]
                    z *= [pos[1][n], pos[0][m]]
                    mu1 += z
                    z *= pos[:, m, n]
                    mu2 += z
#                    z *= pos[:, m, n]
#                    mu3 += z
#                    z *= pos[:, m, n]
#                    mu4 += z
        # If pos is formatted as an mgrid.
        else:
            for m in range(M):
                for n in range(N):
                    W += weights[m, n]
                    z[:] = weights[m, n]
                    z *= pos[::-1, m, n]
                    mu1 += z
                    z *= pos[::-1, m, n]
                    mu2 += z
#                    z *= pos[::-1, m, n]
#                    mu3 += z
#                    z *= pos[::-1, m, n]
#                    mu4 += z
    mu1 /= W
    mu2 /= W
#    mu3 /= W
#    mu4 /= W
#    mu4 += mu1*(-4*mu3 + 3*mu1*(2*mu2 - mu1**2))
#    mu3 += mu1*(-3*mu2 + 2*mu1**2)
    mu2 -= mu1**2
    s = np.sqrt(mu2)
#    mu3 /= mu2*s
#    mu4 /= mu2**2
    return {
        'sum of weights' : W,
        'mean' : mu1,
        'variance' : mu2,
        'standard deviation' : s,
#        'skew' : mu3,
#        'kurtosis' : mu4,
#        'excess kurtosis' : mu4-3.,
        }

# ======================================================================
# Profile maker.
# ======================================================================

def profile(img, grid=False):
    x = img.mean(0)
    y = img.mean(1)
    if grid:
        return [np.ogrid[:x.size], x], [np.ogrid[:y.size], y]
    else:
        return x, y

# ======================================================================
