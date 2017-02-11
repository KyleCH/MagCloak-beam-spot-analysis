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
    Dx = roi[1] - roi[0]
    Dy = roi[3] - roi[2]
    dx = Dx // 2
    dy = Dy // 2
    roi2 = (roi[0]-dx, roi[1]+dx, roi[2]-dy, roi[3]+dy)
    
    img2 = img[roi2[2]:roi2[3], roi2[0]:roi2[1]]
    img2 = img2.mean(axis=2)
    img1 = img2[dy:Dy+dy, dx:Dx+dx]
    img = analysis.cutoff(img1, params['low'], params['high'])
    
    heights, bin_edges = np.histogram(img, bins)
    heights1, bin_edges = np.histogram(img1, bins)
    heights2, bin_edges = np.histogram(img2, bins)
    
    stats = analysis.moments(img, roi)
    stats1 = analysis.moments(img1, roi)
    stats2 = analysis.moments(img2, roi)
    
    plotter.plot_img(
        img=img, img1=img1, img2=img2,
        roi=roi,
        roi2=roi2,
        stats=stats,
        stats1=stats1,
        stats2=stats2,
        saveas=dirs['out']+'i_{:04}.png'.format(serial),
        LX=LX,
        LY=LY,
        )
    # ------------------------------------------------------------------
    plotter.profile0(
        bins=np.mgrid[roi[0]:roi[1]],
        bins2=np.mgrid[roi2[0]:roi2[1]],
        heights=img.sum(axis=0),
        heights1=img1.sum(axis=0),
        heights2=img2.sum(axis=0),
        stats=stats[0],
        stats1=stats1[0],
        stats2=stats2[0],
        saveas=dirs['out']+'x0_{:04}.png'.format(serial),
        )
    plotter.profile0(
        bins=np.mgrid[roi[2]:roi[3]],
        bins2=np.mgrid[roi2[2]:roi2[3]],
        heights=img.sum(axis=1),
        heights1=img1.sum(axis=1),
        heights2=img2.sum(axis=1),
        stats=stats[1],
        stats1=stats1[1],
        stats2=stats2[1],
        saveas=dirs['out']+'y0_{:04}.png'.format(serial),
        )
    # ------------------------------------------------------------------
    plotter.profile0(
        bins=np.mgrid[roi[0]:roi[1]],
        bins2=np.mgrid[roi2[0]:roi2[1]],
        heights=img.mean(axis=0),
        heights1=img1.mean(axis=0),
        heights2=img2.mean(axis=0),
        stats=stats[0],
        stats1=stats1[0],
        stats2=stats2[0],
        saveas=dirs['out']+'x0_{:04}.png'.format(serial),
        )
    plotter.profile0(
        bins=np.mgrid[roi[2]:roi[3]],
        bins2=np.mgrid[roi2[2]:roi2[3]],
        heights=img.mean(axis=1),
        heights1=img1.mean(axis=1),
        heights2=img2.mean(axis=1),
        stats=stats[1],
        stats1=stats1[1],
        stats2=stats2[1],
        saveas=dirs['out']+'y0_{:04}.png'.format(serial),
        )
    # ------------------------------------------------------------------
    plotter.hist(
        bins=bin_edges,
        heights=heights,
        heights1=heights1,
        heights2=heights2,
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
