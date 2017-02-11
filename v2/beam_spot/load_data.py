#!/usr/bin/env python3

import numpy as np
from scipy.ndimage import imread

# ======================================================================
# Read in image file.
# ======================================================================

def image(fname, path, of=None):
    if of is None:
        print('File: {}\n\tPath: {}'.format(fname))
    else:
        of.write('\nFile: {}\n\tPath: {}'.format(fname, path))
    return imread(path)

# ======================================================================
