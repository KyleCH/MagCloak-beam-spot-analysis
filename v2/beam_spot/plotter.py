#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# ======================================================================
# Plot image.
# ======================================================================

def image(img, stats=None, saveas=None, **kwargs):
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    if (stats is not None):
        ax.errorbar(
            stats[0, 0], stats[1, 0],
            xerr=stats[0, 1], yerr=stats[1, 1],
            **kwargs)
    if (img.ndim == 2):
        ly, lx = img.shape
    else:
        ly, lx = img.shape[0:2]
    ax.xaxis.tick_top()
    ax.set_xlim(-.5, lx-.5)
    ax.set_ylim(ly-.5, -.5)
    return fig, ax

# ======================================================================
# Profile plotter.
# ======================================================================

def profile(
        bins, heights, centered=True, fill=False,
        stats=None, cmean='g', cstd='y', **kwargs):
    fig, ax = plt.subplots(1)
    X = np.stack([bins, bins]).T.flatten()
    Y = np.stack([heights, heights]).T.flatten()
    # Center aligned.
    if centered:
        d = .5 * (bins[-1]-bins[-2])
        L = bins[-1] + d
        # Filled.
        if fill:
            X = np.append(X[1:]-d, L)
            ax.fill_between(X, Y, **kwargs)
        # Empty.
        else:
            X = np.append(X-d, [L, L])
            Y = np.append(np.append(0., Y[:]), 0.)
            ax.plot(X, Y, **kwargs)
    # Left aligned.
    else:
        L = 2*bins[-1] - bins[-2]
        # Filled.
        if fill:
            X = np.append(X[1:], L)
            ax.fill_between(X, Y, **kwargs)
        # Empty.
        else:
            X = np.append(X, [L, L])
            Y = np.append(np.append(0., Y[:]), 0.)
            ax.plot(X, Y, **kwargs)
    ax.set_xlim(X.min(), X.max())
    Ymin = Y.min()
    if (Ymin > 0.):
        Ymin = 0.
    ax.set_ylim(Ymin)
    if (stats is not None):
        ylim = ax.get_ylim()
        ax.vlines(
            stats[0],
            ymin=ylim[0],
            ymax=ylim[1],
            colors=cmean,
            label='mean'
            )
        ax.vlines(
            [stats[0]+stats[1], stats[0]-stats[1]],
            ymin=ylim[0],
            ymax=ylim[1],
            colors=cstd,
            label='mean $\pm$ std. dev.'
            )
        ax.legend(loc='best')
    
    return fig, ax

# ======================================================================
# Histogram plotter.
# ======================================================================

def hist(bins, heights, fill=False,**kwargs):
    fig, ax = plt.subplots(1)
    X = np.stack([bins, bins]).T.flatten()
    Y = np.stack([heights, heights]).T.flatten()
    # Filled.
    if fill:
        ax.fill_between(X[1:-1], Y, **kwargs)
    # Empty.
    else:
        Y = np.append(np.append(0., Y[:]), 0.)
        ax.plot(X, Y, **kwargs)
    ax.set_xlim(X.min(), X.max())
    Ymin = Y.min()
    if (Ymin > 0.):
        Ymin = 0.
    ax.set_ylim(Ymin)
    return fig, ax

# ======================================================================
