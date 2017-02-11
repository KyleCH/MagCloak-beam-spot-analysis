#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
#import scipy.ndimage as scindi

# ======================================================================
# Plot 2D image.
# ======================================================================

def plot(serial, img, img_cut, extent, ROIbox, stats, saveas):
    fig, axarr = plt.subplots(1, 2, sharey=False)
    fig.suptitle('Image Serial Number: '+serial)
    # ------------------------------------------------------------------
    axarr[0].set_title('Region of Interest (ROI)')
    axarr[0].set_xlim(extent[0], extent[1])
    axarr[0].set_ylim(extent[3], extent[2])
    axarr[0].imshow(
        img,
        cmap='Greys_r',
        interpolation='none',
        extent=(extent[0], extent[1], extent[3], extent[2]),
        )
    axarr[0].plot(
        [ROIbox[1], ROIbox[0], ROIbox[0], ROIbox[1], ROIbox[1]],
        [ROIbox[3], ROIbox[3], ROIbox[2], ROIbox[2], ROIbox[3]],
        color='#ff0000',
        )
    axarr[0].errorbar(
        stats[0, 0], stats[1, 0],
        xerr=stats[0, 1], yerr=stats[1, 1],
        color='#00ff00',
        )
    # ------------------------------------------------------------------
    axarr[1].set_title('ROI with Thresholding')
    axarr[1].set_xlim(extent[0], extent[1])
    axarr[1].set_ylim(extent[3], extent[2])
    axarr[1].imshow(
        img_cut,
        cmap='Greys_r',
        interpolation='none',
        extent=(extent[0], extent[1], extent[3], extent[2]),
        )
    axarr[1].plot(
        [ROIbox[1], ROIbox[0], ROIbox[0], ROIbox[1], ROIbox[1]],
        [ROIbox[3], ROIbox[3], ROIbox[2], ROIbox[2], ROIbox[3]],
        color='#ff0000',
        )
    axarr[1].errorbar(
        stats[0, 0], stats[1, 0],
        xerr=stats[0, 1], yerr=stats[1, 1],
        color='#00ff00',
        )
    # ------------------------------------------------------------------
    fig.savefig(saveas)
    plt.close()
    return None

# ======================================================================
# Verbose plot (unfinished).
# ======================================================================
#
#bins = np.append(np.append(0, np.mgrid[1:256]-0.5), 255)
#
#def Vplot(img, img_cut, extent, roi, roi_box, stats, bins, heights, saveas):
#    # ------------------------------------------------------------------
#    
#    # ------------------------------------------------------------------
#    fig, axarr = plt.subplots(1, 2, sharey=False)
#    # ------------------------------------------------------------------
#    axarr[0, 0].set_title('Region of Interest (ROI)')
#    axarr[0, 0].imshow(
#        img,
#        cmap='Greys_r',
#        interpolation='none',
#        extent=extent,
#        )
#    axarr[0, 0].set_xlim(extent[0], extent[1])
#    axarr[0, 0].set_ylim(extent[2], extent[3])
#    axarr[0, 0].plot(
#        [roi_box[1], roi_box[0], roi_box[0], roi_box[1], roi_box[1]],
#        [roi_box[3], roi_box[3], roi_box[2], roi_box[2], roi_box[3]],
#        color='#ff0000',
#        )
#    axarr[0, 0].errorbar(
#        stats[0, 0], stats[1, 0],
#        xerr=stats[0, 1], yerr=stats[1, 1],
#        color='#00ff00',
#        )
#    # ------------------------------------------------------------------
#    axarr[0, 0].set_title('ROI with Thresholding')
#    axarr[0, 1].imshow(
#        img_cut, cmap='Greys_r', interpolation='none', extent=extent)
#    axarr[0, 1].set_xlim(extent[0], extent[1])
#    axarr[0, 1].set_ylim(extent[2], extent[3])
#    axarr[0, 1].plot(
#        [roi_box[1], roi_box[0], roi_box[0], roi_box[1], roi_box[1]],
#        [roi_box[3], roi_box[3], roi_box[2], roi_box[2], roi_box[3]],
#        color='#ff0000',
#        )
#    axarr[0, 1].errorbar(
#        stats[0, 0], stats[1, 0],
#        xerr=stats[0, 1], yerr=stats[1, 1],
#        color='#00ff00',
#        )
#    # ------------------------------------------------------------------
#    axarr[1, 0].set_title('Horizantle Profile')
#    h_profile_X = np.arange(roi_box[0]+1, roi_box[1])
#    h_profile_X = (
#        np.stack(
#            [np.append(roi_box[0], X), np.append(X, roi_box[1])]
#            ).T.flatten()
#        )
#    Y = np.stack([heights, heights]).T.flatten()
#    ax.plot(h_profile_X, Y)
#    # ------------------------------------------------------------------
#    axarr[1, 1].set_title('Vertical Profile')
#    
#    # ------------------------------------------------------------------
#    heights, bin_edges = np.histogram(
#        img[roi[2]:roi[3], roi[0]:roi[1]], bins)
#    heights_cut, bin_edges = np.histogram(
#        img_cut[roi[2]:roi[3], roi[0]:roi[1]], bins)
#    hist_X = np.stack([bin_edges, bin_edges]).T.flatten()[1:-1]
#    Y = np.stack([heights, heights]).T.flatten()
#    Y_cut = np.stack([heights, heights]).T.flatten()
#    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#    axarr[2, 0].set_title('Intensity Histogram')
#    axarr[2, 0].plot(hist_X, Y)
#    axarr[2, 0].plot(hist_X, Y_cut)
#    axarr[2, 0].set_yscale('log')
#    axarr[2, 0].set_xlim(hist_X[0], hist_X[-1])
#    axarr[2, 0].set_ylim(0.1)
#    # ------------------------------------------------------------------
#    fig.delaxes(axarr[2, 1])
#    # ------------------------------------------------------------------
#    fig.savefig(saveas)
#    plt.close()
#    return None
#
# ======================================================================
