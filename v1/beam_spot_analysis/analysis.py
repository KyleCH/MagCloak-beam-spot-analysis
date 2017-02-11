#!/usr/bin/env python3

import numpy as np

# ======================================================================
# Statistical moments.
# ======================================================================

def moments_1d(pos, w):
    m = np.zeros(5)
    for n in range(pos.size):
        z = w[n]
        m[0] += z
        z *= pos[n]
        m[1] += z
        z *= pos[n]
        m[2] += z
        z *= pos[n]
        m[3] += z
        z *= pos[n]
        m[4] += z
    m[1:] /= m[0]
    m[4] -= m[1]*(-4*m[3] + 3*m[1]*(2*m[2] - m[1]**2))
    m[3] += m[1]*(-3*m[2] + 2*m[1]**2)
    m[2] -= m[1]**2
    s = np.sqrt(m[2])
    m[3] /= m[2]*s
    m[4] /= m[2]**2
    return {
        'sum of weights' : m[0],
        'mean' : m[1],
        'variance' : m[2],
        'standard deviation' : s,
        'skew' : m[3],
        'kurtosis' : m[4],
        'Fisher kurtosis' : m[4]-3.,
        }

# ======================================================================
# Two-dimensional statistical moments.
# ======================================================================

def moments_2d(pos, w):
    W = 0.
    mu1 = np.zeros(2)
    mu2 = np.zeros(2)
    mu3 = np.zeros(2)
    mu4 = np.zeros(2)
    M, N = pos.shape[1:3]
    for m in range(M):
        for n in range(N):
            W += w[m, n]
            z = pos[:, m, n]*w[m, n]
            mu1 += z
            z *= pos[:, m, n]
            mu2 += z
            z *= pos[:, m, n]
            mu3 += z
            z *= pos[:, m, n]
            mu4 += z
    mu1 /= W
    mu2 /= W
    mu3 /= W
    mu4 /= W
    mu4 += mu1*(-4*mu3 + 3*mu1*(2*mu2 - mu1**2))
    mu3 += mu1*(-3*mu2 + 2*mu1**2)
    mu2 -= mu1**2
    s = np.sqrt(mu2)
    mu3 /= mu2*s
    mu4 /= mu2**2
    return {
        'sum of weights' : W,
        'mean' : mu1,
        'variance' : mu2,
        'standard deviation' : s,
        'skew' : mu3,
        'kurtosis' : mu4,
        'Fisher kurtosis' : mu4-3.,
        }

# ======================================================================
