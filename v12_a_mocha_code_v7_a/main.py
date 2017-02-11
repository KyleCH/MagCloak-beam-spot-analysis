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
    
    roi1 = params['ROI1']
    roi2 = params['ROI2']
    img0 = scindi.imread(fname)
    roi0 = img0.shape[0:2]
    roi0 = (0, roi0[1], 0, roi0[0])
    img0 = img0.mean(axis=2)
    
#    img1 = img0[roi1[2]:roi1[3], roi1[0]:roi1[1]]
#    img2 = img0[roi2[2]:roi2[3], roi2[0]:roi2[1]]
    
#    heights0, bin_edges = np.histogram(img0, bins)
    heights1, bin_edges = np.histogram(
        img0[roi1[2]:roi1[3], roi1[0]:roi1[1]], bins)
    heights2, bin_edges = np.histogram(
        img0[roi2[2]:roi2[3], roi2[0]:roi2[1]], bins)
    
    plotter.plot_img(
        img=img0,
        roi=roi0,
        saveas=dirs['out']+'img0_{:04}.png'.format(serial))
    plotter.plot_img(
        img=img0[roi1[2]:roi1[3], roi1[0]:roi1[1]],
        roi=roi1,
        saveas=dirs['out']+'img1_{:04}.png'.format(serial))
    plotter.plot_img(
        img=img0[roi2[2]:roi2[3], roi2[0]:roi2[1]],
        roi=roi2,
        saveas=dirs['out']+'img2_{:04}.png'.format(serial))
    
#    plotter.hist(
#        bins=bin_edges,
#        heights=heights0,
#        saveas=dirs['out']+'hist0_{:04}.png'.format(serial),
#        )
    plotter.hist(
        bins=bin_edges,
        heights=heights1,
        saveas=dirs['out']+'hist1_{:04}.png'.format(serial),
        )
    plotter.hist(
        bins=bin_edges,
        heights=heights2,
        saveas=dirs['out']+'hist2_{:04}.png'.format(serial),
        )
    
    return None

# ======================================================================
# Run.
# ======================================================================

if (__name__ == '__main__'):
    test = False
    yes = ['True', 'true', 'Yes', 'yes', 'Y', 'y', '1']
    no = ['False', 'false', 'No', 'no', 'N', 'n', '0']
    
    roi1 = (2290, 2840, 1240, 1650)
    Dx = roi1[1] - roi1[0]
    Dy = roi1[3] - roi1[2]
    dx = Dx // 2
    dy = Dy // 2
    roi2 = (roi1[0]-dx, roi1[1]+dx, roi1[2]-dy, roi1[3]+dy)
    modio.run(
        process=process,
        params={
            'low' : 25,
            'high' : 100,
            'ROI1' : roi1,
            'ROI2' : roi2,
            },
        test=test,
        )
