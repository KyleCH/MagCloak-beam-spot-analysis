#!/usr/bin/env python3

import numpy as np
from scipy.ndimage import imread

from . import analysis
from . import colors
from . import plotter

# ======================================================================
# Read in image file.
# ======================================================================

def image(fname):
    img = imread(fname)
    ly, lx = img.shape[0:2]
#    I = colors.I_RGB(r=img[:, :, 0], g=img[:, :, 1], b=img[:, :, 2])
    I = colors.I_RGB_2(img)
    stats = analysis.moments_2d(np.mgrid[0:ly, 0:lx], I)
    print(fname)
    print(stats)
    im, fig, ax = plotter.beam_spot(img)
    er = plotter.centroid(stats['mean'], stats['standard deviation'], fig, ax)
    return fig, ax
