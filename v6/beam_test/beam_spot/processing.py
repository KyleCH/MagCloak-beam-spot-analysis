#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from . import analysis
from . import colors
from . import modio
from . import plotter

# ======================================================================
# Perform basic processing.
# ======================================================================

def basic(fname, img=None, use='I', color_info=None):
    if (img is None):
        img = modio.image(fname)
    if (color_info is None):
        color_info = colors.from_RGB_wo_vect(img)
    stats = analysis.moments_2d(color_info[use])
    modio.stats(stats)
    plot_stats = np.asarray([
        [stats['mean'][0], stats['standard deviation'][0],],
        [stats['mean'][1], stats['standard deviation'][1],],
        ])
    heights, bin_edges = np.histogram(
        color_info[use],
        bins=np.append(np.append(0., np.mgrid[1:256]-0.5), 255.),
        )
    x_profile, y_profile = analysis.profile(color_info[use], grid=True)
    
    fig, ax = plotter.image(img, plot_stats)
    fig.savefig('{}_plot.png'.format(fname[:-4]))
    plt.close()
    
    figu, axu = plotter.image(color_info[use], plot_stats)
    figu.savefig('{}_{}.png'.format(fname[:-4], use))
    plt.close()
    
    figh, axh = plotter.hist(bin_edges, heights)
    figh.savefig('{}_{}_hist.png'.format(fname[:-4], use))
    plt.close()
    
    figx, axx = plotter.profile(x_profile[0], x_profile[1],
        stats=plot_stats[0])
    figx.savefig('{}_{}_x.png'.format(fname[:-4], use))
    plt.close()
    
    figy, axy = plotter.profile(y_profile[0], y_profile[1],
        stats=plot_stats[1])
    figy.savefig('{}_{}_y.png'.format(fname[:-4], use))
    plt.close()
    
#    fig.show()
#    figu.show()
#    figx.show()
#    figy.show()
#    input('')
    return 0

# ======================================================================
# Binary histogram maker.
# ======================================================================

def binary_hist(
        fname,
        use=['I'], img=None, color_info=None,
        odir=modio.dirs['out']
        ):
    if (img is None):
        img = modio.image(fname)
    if (color_info is None):
        color_info = colors.from_RGB_wo_vect(img)
    start = fname.rfind('/')
    stop = fname.rfind('.')
    name = odir + fname[start+1:stop]
    for u in use:
        heights, bin_edges = np.histogram(
            color_info[u],
            bins=np.append(np.append(0., np.mgrid[1:256]-0.5), 255.),
            )
        x_profile, y_profile = analysis.profile(color_info[u], grid=True)
        
        np.save('{}_{}.npy'.format(name, u), color_info[u])
        np.save('{}_{}_x.npy'.format(name, u), x_profile)
        np.save('{}_{}_y.npy'.format(name, u), y_profile)
        
        plotter.image(
            color_info[u],
            saveas='{}_{}.png'.format(name, u),
            )
        
        plotter.hist(
            bin_edges, heights,
            saveas='{}_{}_hist.png'.format(name, u),
            )
        
        plotter.profile(
            x_profile[0], x_profile[1],
            saveas='{}_{}_x.png'.format(name, u),
            )
        
        plotter.profile(
            y_profile[0], y_profile[1],
            saveas='{}_{}_y.png'.format(name, u),
            )
    
    return 0

# ======================================================================
