#!/usr/bin/env python3

import numpy as np
import scipy.ndimage as scindi

import analysis
import modio
import plotter

# ======================================================================

bins = np.append(np.append(0, np.mgrid[1:256]-0.5), 255)

# ======================================================================
# Process data.
# ======================================================================

def process(dirs, fname, serial, current, params):
    
    roi = params['ROI']
    LX = (roi[0] - 0.5, roi[1] - 0.5)
    LY = (roi[2] - 0.5, roi[3] - 0.5)
    
    # Load image, convert to intensity, calculate statistics, and plot.
    img = scindi.imread(fname)
    img = img.mean(axis=2)
    
    # Restrict to ROI, calcualte statistics, and plot.
    img = img[roi[2]:roi[3], roi[0]:roi[1]]
    
    # Apply cutoffs, calcualte statistics, and plot.
    img = analysis.cutoff(img, params['low'], params['high'])
    stats = analysis.moments(img, roi)
    plotter.plot_img(
        img,
        serial,
        roi=roi,
        stats=stats,
        saveas=dirs['out']+'i_{:04}.png'.format(serial),
        LX=LX,
        LY=LY,
        )
    plotter.profile(
        np.mgrid[roi[0]:roi[1]],
        img.mean(axis=0),
        stats=stats[0],
        saveas=dirs['out']+'x_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[roi[2]:roi[3]],
        img.mean(axis=1),
        stats=stats[1],
        saveas=dirs['out']+'y_{:04}.png'.format(serial),
        )
    heights, bin_edges = np.histogram(img, bins)
    plotter.hist(
        bins=bin_edges,
        heights=heights,
        saveas=dirs['out']+'h_{:04}.png'.format(serial),
        )
    
    return stats

# ======================================================================
# Run.
# ======================================================================

if (__name__ == '__main__'):
    test = True
    yes = ['True', 'true', 'Yes', 'yes', 'Y', 'y', '1']
    no = ['False', 'false', 'No', 'no', 'N', 'n', '0']
    modio.run(
        process=process,
        params={
            'low' : 25,
            'high' : 100,
            'ROI' : (2290, 2840, 1240, 1650),
            },
        test=test,
        )
