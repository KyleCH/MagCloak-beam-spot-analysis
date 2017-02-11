#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Plot 2D image.
# ======================================================================

def plot_img(
        img, img1, img2,
        roi, roi2,
        stats, stats1, stats2,
        saveas,
        LX, LY,
        ):
    fig, axarr = plt.subplots(2, 2, sharex=False, sharey=False)
    fig.delaxes(axarr[1, 1])
    axarr[0, 0].imshow(
        img,
        cmap='Greys_r',
        interpolation='none',
        extent=roi
        )
    axarr[0, 0].errorbar(
        stats[0, 0], stats[1, 0],
        xerr=stats[0, 1], yerr=stats[1, 1],
        color='#00ff00',
        label='centroid',
        )
    axarr[0, 1].imshow(
        img1,
        cmap='Greys_r',
        interpolation='none',
        extent=roi
        )
    axarr[0, 1].errorbar(
        stats1[0, 0], stats1[1, 0],
        xerr=stats1[0, 1], yerr=stats1[1, 1],
        color='#00ff00',
        label='centroid',
        )
    axarr[1, 0].imshow(
        img2,
        cmap='Greys_r',
        interpolation='none',
        extent=roi2
        )
    axarr[1, 0].errorbar(
        stats2[0, 0], stats2[1, 0],
        xerr=stats2[0, 1], yerr=stats2[1, 1],
        color='#00ff00',
        label='centroid',
        )
    axarr[0, 0].xaxis.tick_top()
    axarr[0, 0].set_xlim(LX)
    axarr[0, 0].set_ylim(LY)
    axarr[0, 1].xaxis.tick_top()
    axarr[0, 1].set_xlim(LX)
    axarr[0, 1].set_ylim(LY)
    axarr[1, 0].xaxis.tick_top()
    axarr[1, 0].set_xlim(LX)
    axarr[1, 0].set_ylim(LY)
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Profile plotter 0.
# ======================================================================

def profile0(
        bins, bins2,
        heights, heights1, heights2,
        stats, stats1, stats2,
        saveas,
        ):
    L = bins[-1] + 0.5
    L2 = bins2[-1] + 0.5
    X = np.append(np.stack([bins, bins]).T.flatten()[1:], [L])
    X2 = np.append(np.stack([bins2, bins2]).T.flatten()[1:], [L2])
    Y = nnp.stack([heights, heights]).T.flatten()
    Y1 = np.stack([heights1, heights1]).T.flatten()
    Y2 = np.stack([heights2, heights2]).T.flatten()
    fig, ax = plt.subplots(1)
    ax.plot(
        X, Y,
        color='#0000ff',
        label='processed data',
        )
    ax.plot(
        X, Y1,
        color='#00ff00',
        label='restricted',
        )
    ax.plot(
        X2, Y2,
        color='#ff0000',
        label='semi-restricted',
        )
    ax.set_xlim(X2[0], X2[-1])
    ylim = ax.get_ylim()
    ax.vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    ax.vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyle='dashed',
        label='mean $\pm$ std. dev.'
        )
    ax.vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    ax.vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyle='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    ax.vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    ax.vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyle='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
#    ax.legend(loc='best')
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Profile plotter 1.
# ======================================================================

def profile1(
        bins, bins2,
        mean, mean1, mean2,
        maxima, maxima1, maxima2,
        stats, stats1, stats2,
        saveas,
        ):
    L = bins[-1] + 0.5
    L2 = bins2[-1] + 0.5
    X = np.append(np.stack([bins, bins]).T.flatten()[1:], [L])
    X2 = np.append(np.stack([bins2, bins2]).T.flatten()[1:], [L2])
    Y = np.stack([mean, mean]).T.flatten()
    Y1 = np.stack([mean1, mean1]).T.flatten()
    Y2 = np.stack([mean2, mean2]).T.flatten()
    Z = np.stack([maxima, maxima]).T.flatten()
    Z1 = np.stack([maxima1, maxima1]).T.flatten()
    Z2 = np.stack([maxima2, maxima2]).T.flatten()
    fig, axarr = plt.subplots(2, 2, sharex=False, sharey=False)
    fig.delaxes(axarr[0, 1])
    # ------------------------------------------------------------------
    axarr[0, 0].plot(
        X, Y,
        color='#0000ff',
        label='processed mean',
        )
    axarr[0, 0].plot(
        X, Y1,
        color='#00ff00',
        label='restricted mean',
        )
    axarr[0, 0].plot(
        X2, Y2,
        color='#ff0000',
        label='semi-restricted mean',
        )
    axarr[0, 0].set_xlim(X2[0], X2[-1])
    ylim = axarr[0, 0].get_ylim()
    axarr[0, 0].vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    axarr[0, 0].vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyles='dashed',
        label='mean $\pm$ std. dev.'
        )
    axarr[0, 0].vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    axarr[0, 0].vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyles='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    axarr[0, 0].vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    axarr[0, 0].vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyles='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
    # ------------------------------------------------------------------
    axarr[1, 0].plot(
        X, Y,
        color='#0000ff',
        label='processed mean',
        )
    axarr[1, 0].plot(
        X, Y1,
        color='#00ff00',
        label='restricted mean',
        )
    axarr[1, 0].plot(
        X2, Y2,
        color='#ff0000',
        label='semi-restricted mean',
        )
    axarr[1, 0].set_xlim(X2[0], X2[-1])
    ylim = axarr[1, 0].get_ylim()
    axarr[1, 0].vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    axarr[1, 0].vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyles='dashed',
        label='mean $\pm$ std. dev.'
        )
    axarr[1, 0].vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    axarr[1, 0].vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyles='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    axarr[1, 0].vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    axarr[1, 0].vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyles='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
    # ------------------------------------------------------------------
    axarr[1, 1].plot(
        X, Z,
        color='#0000ff',
        linestyle='--',
        label='processed data maxima',
        )
    axarr[1, 1].plot(
        X, Z1,
        color='#00ff00',
        linestyle='--',
        label='restricted maxima',
        )
    axarr[1, 1].plot(
        X2, Z2,
        color='#ff0000',
        linestyle='--',
        label='semi-restricted maxima',
        )
    axarr[1, 1].set_xlim(X2[0], X2[-1])
    ylim = axarr[1, 1].get_ylim()
    axarr[1, 1].vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    axarr[1, 1].vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyles='dashed',
        label='mean $\pm$ std. dev.'
        )
    axarr[1, 1].vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    axarr[1, 1].vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyles='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    axarr[1, 1].vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    axarr[1, 1].vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyles='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
    # ------------------------------------------------------------------
#    axarr[].legend(loc='best')
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Profile plotter 2.
# ======================================================================

def profile2(
        bins, bins2,
        mean, mean1, mean2,
        maxima, maxima1, maxima2,
        stats, stats1, stats2,
        saveas,
        ):
    L = bins[-1] + 0.5
    L2 = bins2[-1] + 0.5
    X = np.append(np.stack([bins, bins]).T.flatten()[1:], [L])
    X2 = np.append(np.stack([bins2, bins2]).T.flatten()[1:], [L2])
    Y = np.stack([mean, mean]).T.flatten()
    Y1 = np.stack([mean1, mean1]).T.flatten()
    Y2 = np.stack([mean2, mean2]).T.flatten()
    Z = np.stack([maxima, maxima]).T.flatten()
    Z1 = np.stack([maxima1, maxima1]).T.flatten()
    Z2 = np.stack([maxima2, maxima2]).T.flatten()
    fig, axarr = plt.subplots(2, 2, sharex=False, sharey=False)
    # ------------------------------------------------------------------
    axarr[0, 0].plot(
        X, Y,
        color='#0000ff',
        label='processed mean',
        )
    axarr[0, 0].plot(
        X, Y1,
        color='#00ff00',
        label='restricted mean',
        )
    axarr[0, 0].plot(
        X2, Y2,
        color='#ff0000',
        label='semi-restricted mean',
        )
    axarr[0, 0].plot(
        X, Z,
        color='#0000ff',
        linestyle='dashed',
        label='processed data maxima',
        )
    axarr[0, 0].plot(
        X, Z1,
        color='#00ff00',
        linestyle='dashed',
        label='restricted maxima',
        )
    axarr[0, 0].plot(
        X2, Z2,
        color='#ff0000',
        linestyle='dashed',
        label='semi-restricted maxima',
        )
    axarr[0, 0].set_xlim(X2[0], X2[-1])
    ylim = axarr[0, 0].get_ylim()
    axarr[0, 0].vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    axarr[0, 0].vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyles='dashed',
        label='mean $\pm$ std. dev.'
        )
    axarr[0, 0].vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    axarr[0, 0].vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyles='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    axarr[0, 0].vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    axarr[0, 0].vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyles='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
    # ------------------------------------------------------------------
    axarr[0, 1].plot(
        X, Y,
        color='#0000ff',
        label='processed mean',
        )
    axarr[0, 1].plot(
        X, Z,
        color='#0000ff',
        linestyle='--',
        label='processed data maxima',
        )
    axarr[0, 1].set_xlim(X2[0], X2[-1])
    ylim = axarr[0, 1].get_ylim()
    axarr[0, 1].vlines(
        stats[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        label='mean'
        )
    axarr[0, 1].vlines(
        [stats[0]+stats[1], stats[0]-stats[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#0000ff',
        linestyles='dashed',
        label='mean $\pm$ std. dev.'
        )
    # ------------------------------------------------------------------
    axarr[1, 0].plot(
        X, Y1,
        color='#00ff00',
        label='restricted mean',
        )
    axarr[1, 0].plot(
        X, Z1,
        color='#00ff00',
        linestyle='dashed',
        label='restricted maxima',
        )
    axarr[1, 0].set_xlim(X2[0], X2[-1])
    ylim = axarr[1, 0].get_ylim()
    axarr[1, 0].vlines(
        stats1[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        label='mean 1'
        )
    axarr[1, 0].vlines(
        [stats1[0]+stats1[1], stats1[0]-stats1[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#00ff00',
        linestyles='dashed',
        label='mean 1 $\pm$ std. dev. 1'
        )
    # ------------------------------------------------------------------
    axarr[1, 1].plot(
        X2, Y2,
        color='#ff0000',
        label='semi-restricted mean',
        )
    axarr[1, 1].plot(
        X2, Z2,
        color='#ff0000',
        linestyle='--',
        label='semi-restricted maxima',
        )
    axarr[1, 1].set_xlim(X2[0], X2[-1])
    ylim = axarr[1, 1].get_ylim()
    axarr[1, 1].vlines(
        stats2[0],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        label='mean 2'
        )
    axarr[1, 1].vlines(
        [stats2[0]+stats2[1], stats2[0]-stats2[1]],
        ymin=ylim[0],
        ymax=ylim[1],
        colors='#ff0000',
        linestyles='dashed',
        label='mean 2 $\pm$ std. dev. 2'
        )
    # ------------------------------------------------------------------
#    axarr[].legend(loc='best')
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Histogram plotter.
# ======================================================================

def hist(
        bins,
        heights, heights1, heights2,
        saveas,
        ):
    fig, axarr = plt.subplots(1, 2, sharey=False)
    X = np.stack([bins, bins]).T.flatten()[1:-1]
    Y = np.stack([heights, heights]).T.flatten()
    Y1 = np.stack([heights1, heights1]).T.flatten()
    Y2 = np.stack([heights2, heights2]).T.flatten()
    axarr[0].plot(
        X, Y,
        color='#0000ff',
        label='processed data')
    axarr[0].plot(
        X, Y1,
        color='#00ff00',
        label='restricted')
    axarr[0].plot(
        X, Y2,
        color='#ff0000',
        label='semi-restricted')
    axarr[1].plot(
        X, Y,
        color='#0000ff',
        label='processed data')
    axarr[1].plot(
        X, Y1,
        color='#00ff00',
        label='restricted')
    axarr[0].set_yscale('log')
    axarr[0].set_xlim(X[0], X[-1])
    axarr[0].legend(loc='best')
    axarr[1].set_yscale('log')
    axarr[1].set_xlim(X[0], X[-1])
    axarr[1].legend(loc='best')
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
