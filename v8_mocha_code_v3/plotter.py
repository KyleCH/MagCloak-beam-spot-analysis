#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Plot 2D image.
# ======================================================================

def plot_img(img, serial, current=None, stats=None, roi=None, saveas=None):
    fig, ax = plt.subplots(1)
#    if (current is not None):
#        fig.suptitle('Current = {:+7.3} A'.format(current))
#    ax.set_title('Serial Number: {:04}'.format(serial))
    ax.imshow(img, cmap='Greys_r')
    if (roi is not None):
        ax.plot(
            [
                roi[0, 0]-0.5,
                roi[0, 1]+0.5,
                roi[0, 1]+0.5,
                roi[0, 0]-0.5,
                roi[0, 0]-0.5,
                ],
            [
                roi[1, 0]-0.5,
                roi[1, 0]-0.5,
                roi[1, 1]+0.5,
                roi[1, 1]+0.5,
                roi[1, 0]-0.5,
                ],
            color='r',
#            markerstyle='',
            label='ROI',
            )
    if (stats is not None):
        ax.errorbar(
            stats[0, 0], stats[1, 0],
            xerr=stats[0, 1], yerr=stats[1, 1],
            color='b',
#            label='statistics',
            )
    ly, lx = img.shape
    ax.xaxis.tick_top()
    ax.set_xlim(-.5, lx-.5)
    ax.set_ylim(ly-.5, -.5)
    if (saveas is None):
        return fig, ax
    else:
        fig.savefig(saveas)
        plt.close()
        return None

# ======================================================================
# Profile plotter.
# ======================================================================

def profile(
        bins, heights, centered=True, fill=False,
        stats=None, roi=None, cmean='g', cstd='y', saveas=None, **kwargs):
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
    if (roi is not None):
        ax.vlines(
            [roi[0], roi[1]],
            ymin=ylim[0],
            ymax=ylim[1],
            colors='r',
            label='ROI'
            )
    if (saveas is None):
        return fig, ax
    else:
        fig.savefig(saveas)
        plt.close()
        return None

# ======================================================================
# Histogram plotter.
# ======================================================================

def hist(bins, heights, figax=None, fill=False, saveas=None, **kwargs):
    if (figax is None):
        fig, ax = plt.subplots(1)
    else:
        fig = figax[0]
        ax = figax[1]
    X = np.stack([bins, bins]).T.flatten()
    Y = np.stack([heights, heights]).T.flatten()
    # Filled.
    if fill:
        ax.fill_between(X[1:-1], Y, **kwargs)
    # Empty.
    else:
        Y = np.append(np.append(0., Y[:]), 0.)
        ax.plot(X, Y, **kwargs)
#    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(X.min(), X.max())
    Ymin = Y.min()
    if (Ymin > 0.):
        Ymin = 0.
    ax.set_ylim(Ymin)
    if (saveas is None):
        return fig, ax
    else:
        fig.savefig(saveas)
        plt.close()
        return None

# ======================================================================
