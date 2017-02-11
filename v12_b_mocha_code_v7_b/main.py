#!/usr/bin/env python3

import numpy as np
import scipy.ndimage as scindi

import analysis
import modio
import plotter

# ======================================================================
# Process data.
# ======================================================================

def process(dirs, fname, serial, low, high, ROI, ROIbox, SOI, ind, extent):
    img = scindi.imread(fname)[SOI[2]:SOI[3], SOI[0]:SOI[1], :].mean(axis=2)
    img_cut = analysis.cutoff(
        a=img,
        low=low,
        high=high,
        )
    stats = analysis.moments(
        w=img_cut[ind[2]:ind[3], ind[0]:ind[1]],
        ROI=ROI,
        )
#    stats = np.zeros((2, 2))
    s = '{:04}'.format(serial)
    plotter.plot(
        serial=s,
        img=img,
        img_cut=img_cut,
        extent=extent,
        ROIbox=ROIbox,
        stats=stats,
        saveas=dirs['out']+s+'.png',
        )
    return stats

# ======================================================================
# Run.
# ======================================================================

if (__name__ == '__main__'):
    test = False
    ROI = np.array([2300, 2900, 1200, 2000])
    dx = (ROI[1] - ROI[0])//2
    dy = (ROI[3] - ROI[2])//2
    SOI = np.copy(ROI)
    SOI[0] -= dx
    SOI[1] += dx
    SOI[2] -= dy
    SOI[3] += dy
    ind = np.copy(ROI)
    ind[0:2] -= SOI[0]
    ind[2:4] -= SOI[2]
    ROIbox = ROI - 0.5
    extent = SOI - 0.5
    modio.run(
        process,
        {
            'low' : 15,
            'high' : 255,
            'ROI' : ROI,
            'SOI' : SOI,
            'ind' : ind,
            'ROIbox' : ROIbox,
            'extent' : extent,
            },
        test,
        )
