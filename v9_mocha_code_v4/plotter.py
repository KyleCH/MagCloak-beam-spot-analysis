#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Plot 2D image.
# ======================================================================

def plot_img(img, serial, roi, stats, saveas, LX, LY):
    fig, ax = plt.subplots(1)
    ax.imshow(
        img,
        cmap='Greys_r',
        interpolation='none',
        extent=roi
        )
    ax.errorbar(
        stats[0, 0], stats[1, 0],
        xerr=stats[0, 1], yerr=stats[1, 1],
        color='#00ff00',
        label='centroid',
        )
    ax.xaxis.tick_top()
    ax.set_xlim(LX)
    ax.set_ylim(LY)
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Profile plotter.
# ======================================================================

def profile(bins, heights, stats, saveas):
    d = .5 * (bins[-1]-bins[-2])
    L = bins[-1] + d
    X = np.append(np.stack([bins, bins]).T.flatten(), [L, L])
    Y = np.append(np.append(0., np.stack([heights, heights]).T.flatten()), 0.)
    fig, ax = plt.subplots(1)
    ax.plot(X, Y)
    ax.set_xlim(X[0], X[-1])
    ylim = ax.get_ylim()
    ax.vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean'
        )
    ax.vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ffff00',
        label='mean $\pm$ std. dev.'
        )
    ax.legend(loc='best')
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Histogram plotter.
# ======================================================================

def hist(bins, heights, saveas):
    fig, ax = plt.subplots(1)
    X = np.stack([bins, bins]).T.flatten()
    Y = np.append(np.append(0., np.stack([heights, heights]).T.flatten()), 0.)
    ax.plot(X, Y)
    ax.set_yscale('log')
    ax.set_xlim(X[0], X[-1])
    ax.set_ylim(0)
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
