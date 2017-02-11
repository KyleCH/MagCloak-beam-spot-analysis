#!/usr/bin/env python3

import numpy as np
from scipy.ndimage import imread

from . import analysis

def set_p(ofile):
    if (ofile is None):
        p = print
    else:
        def p(string):
            return ofile.write('\n{}'.format(string))
    return p

# ======================================================================
# Read in image file.
# ======================================================================

def image(fname, path=None, ofile=None):
    p = set_p(ofile)
    if path is None:
        p('File: {}\n'.format(fname))
        return imread(fname)
    else:
        p('File: {}\n\tPath: {}'.format(fname, path))
        return imread(path)

# ======================================================================
# Output statistics.
# ======================================================================

def stats(data, ofile=None, add_keys=None):
    p = set_p(ofile)
    if (add_keys is None):
        keys = analysis.moment_keys
    else:
        keys = analysis.moment_keys + add_keys
    for key in keys:
        if key in data:
            p('\t{}: {}'.format(key, data[key]))
    return None

# ======================================================================
