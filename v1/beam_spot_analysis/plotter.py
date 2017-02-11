#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# ======================================================================
# Show beam spot image.
# ======================================================================

def beam_spot(img, ax=None, **kwargs):
    not_passed = (ax is None)
    if not_passed:
        fig, ax = plt.subplots(1)
    imgplot = ax.imshow(img, interpolation='none', **kwargs)
    if not_passed:
        return imgplot, fig, ax
    else:
        return imgplot

# ======================================================================
# Show centroid and width.
# ======================================================================

def centroid(mean, std, fig=None, ax=None, **kwargs):
    not_passed = ((fig is None) or (ax is None))
    if not_passed:
        fig, ax = plt.subplots(1)
    errbar = ax.errorbar(mean[1], mean[0], xerr=std[1], yerr=std[0], **kwargs)
    if not_passed:
        return errbar, fig, ax
    else:
        return errbar

# ======================================================================
# Standard plot.
# ======================================================================



