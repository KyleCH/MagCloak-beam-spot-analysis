#!/usr/bin/env python3

import numpy as np
import scipy.ndimage as scindi

import analysis
import modio
import plotter

# ======================================================================
# Process data.
# ======================================================================

def process(dirs, fname, serial, current, params):
    
    # Load image, convert to intensity, calculate statistics, and plot.
    img = scindi.imread(fname)
    img = img.mean(axis=2)
    stats = analysis.moments(img)
    plotter.plot_img(
        img, serial, current, stats=stats,
        saveas=dirs['out']+'i_{:04}.png'.format(serial),
        )
    ly, lx = img.shape
    plotter.profile(
        np.mgrid[0:lx], img.mean(axis=0),
        stats=stats[0],
        saveas=dirs['out']+'x_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:ly], img.mean(axis=1),
        stats=stats[1],
        saveas=dirs['out']+'y_{:04}.png'.format(serial),
        )
    bins = np.append(np.append(0, np.mgrid[1:256]-0.5), 255)
    heights, bin_edges = np.histogram(img, bins)
    plotter.hist(
        bins=bin_edges, heights=heights,
        saveas=dirs['out']+'h_{:04}.png'.format(serial),
        )
    
    # Restrict to ROI, calcualte statistics, and plot.
    roi = params['ROI']
    stats = analysis.moments(img, roi)
    plotter.plot_img(
        img, serial, current, stats=stats,
        roi=roi,
        saveas=dirs['out']+'i_ROI_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:lx],
        img[roi[1, 0]:roi[1, 1], :].mean(axis=0),
        stats=stats[0],
        roi=roi[0],
        saveas=dirs['out']+'x_ROI_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:ly], img[:, roi[0, 0]:roi[0, 1]].mean(axis=1),
        stats=stats[1],
        roi=roi[1],
        saveas=dirs['out']+'y_ROI_{:04}.png'.format(serial),
        )
    heights, bin_edges = np.histogram(
        img[roi[1, 0]:roi[1,1], roi[0, 0]:roi[0,1]],
        bins,
        )
    plotter.hist(
        bins=bin_edges, heights=heights,
        saveas=dirs['out']+'h_ROI_{:04}.png'.format(serial),
        )
    
    # Apply cutoffs, calcualte statistics, and plot.
    img = analysis.cutoff(img, params['low'], params['high'])
    stats = analysis.moments(img)
    plotter.plot_img(
        img, serial, current, stats=stats,
        saveas=dirs['out']+'i_Cut_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:lx], img.mean(axis=0),
        stats=stats[0],
        saveas=dirs['out']+'x_Cut_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:ly], img.mean(axis=1),
        stats=stats[1],
        saveas=dirs['out']+'y_Cut_{:04}.png'.format(serial),
        )
    heights, bin_edges = np.histogram(img, bins)
    plotter.hist(
        bins=bin_edges, heights=heights,
        saveas=dirs['out']+'h_Cut_{:04}.png'.format(serial),
        )
    
    # Restrict to ROI, calcualte statistics, and plot.
    roi = params['ROI']
    stats = analysis.moments(img, roi)
    plotter.plot_img(
        img, serial, current, stats=stats,
        roi=roi,
        saveas=dirs['out']+'i_Cut_ROI_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:lx], img[roi[1, 0]:roi[1, 1], :].mean(axis=0),
        stats=stats[0],
        roi=roi[0],
        saveas=dirs['out']+'x_Cut_ROI_{:04}.png'.format(serial),
        )
    plotter.profile(
        np.mgrid[0:ly], img[:, roi[0, 0]:roi[0, 1]].mean(axis=1),
        stats=stats[1],
        roi=roi[1],
        saveas=dirs['out']+'y_Cut_ROI_{:04}.png'.format(serial),
        )
    heights, bin_edges = np.histogram(
        img[roi[1, 0]:roi[1,1], roi[0, 0]:roi[0,1]],
        bins,
        )
    plotter.hist(
        bins=bin_edges, heights=heights,
        saveas=dirs['out']+'h_Cut_ROI_{:04}.png'.format(serial),
        )
    
    return stats

# ======================================================================
# Run.
# ======================================================================

if (__name__ == '__main__'):
    #test = input('Test\n>>> ')
    test = '0'
    yes = ['True', 'true', 'Yes', 'yes', 'Y', 'y', '1']
    no = ['False', 'false', 'No', 'no', 'N', 'n', '0']
    if (test in yes):
        test = True
    elif (test in no):
        test = False
    else:
        print(
            'Invalid input:\n\tCould not understand input "{}".\n'.format(test)
            + '\tAcceptable input are:\n\t\t{}\n\t\t{}'.format(yes, no)
            )
    modio.run(
        process=process,
        params={
            'low' : 25,
            'high' : 100,
            'ROI' : np.array([[2290, 2840], [1240, 1650]], dtype=np.int16),
#            'sigma' : 51,
            },
        test=test,
        )
