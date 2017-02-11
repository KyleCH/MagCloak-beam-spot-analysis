#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Plot 2D image.
# ======================================================================

def plot_img(img, roi, saveas):
    fig, ax = plt.subplots(1)
    ax.imshow(img, cmap='Greys_r', interpolation='none', extent=roi)
    ax.xaxis.tick_top()
    ax.set_xlim(roi[0]-0.5, roi[1]-0.5)
    ax.set_ylim(roi[2]-0.5, roi[3]-0.5)
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Histogram plotter.
# ======================================================================

def hist(bins, heights, saveas):
    fig, ax = plt.subplots(1)
    X = np.stack([bins, bins]).T.flatten()[1:-1]
    Y = np.stack([heights, heights]).T.flatten()
    ax.plot(X, Y, color='#0000ff')
    ax.set_yscale('log')
    ax.set_xlim(X[0], X[-1])
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
