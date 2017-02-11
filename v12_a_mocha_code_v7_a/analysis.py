#!/usr/bin/env python3

import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Calculate moments.
# ======================================================================

def moments(w, roi, extra=False):
    W = 0.
    m1 = np.zeros(2)
    m2 = np.zeros(2)
    z = np.empty(2)
    if extra:
        for y in range(roi[2], roi[3]):
            for x in range(roi[0], roi[1]):
                W += w[y, x]
                z[:] = w[y, x]
                z[:] *= [x, y]
                m1 += z
                z[:] *= [x, y]
                m2 += z
    else:
        for i, y in enumerate(range(roi[2], roi[3])):
            for j, x in enumerate(range(roi[0], roi[1])):
                W += w[i, j]
                z[:] = w[i, j]
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
