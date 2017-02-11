#!/usr/bin/env python3

import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Calculate moments.
# ======================================================================

def moments(w, roi=None):
    if (roi is None):
        roi = np.asarray(
            [
                [0, w.shape[1]],
                [0, w.shape[0]],
                ]
            )
    W = 0.
    m1 = np.zeros(2)
    m2 = np.zeros(2)
    z = np.empty(2)
    for y in range(roi[1, 0], roi[1, 1]):
        for x in range(roi[0, 0], roi[0, 1]):
            W += w[y, x]
            z[:] = w[y, x]
            z[:] *= [x, y]
            m1 += z
            z[:] *= [x, y]
            m2 += z
    m1 /= W
    m2 /= W
    m2 -= m1**2
    std = np.sqrt(m2)
    return np.asarray(
        [
            [m1[0], std[0]],
            [m1[1], std[1]],
            ]
        )

# ======================================================================
# Cutoff algorithm.
# ======================================================================

def cut(a, low=0, high=255):
    if ((a < low) or (a > high)):
        return 0
    else:
        return a

cutoff = np.vectorize(cut, excluded=('low', 'high'))

# ======================================================================
