#!/usr/bin/env python3

import glob
import os

import numpy as np
from scipy.ndimage import imread

from .analysis import moment_keys

# ======================================================================
# Parameters.
# ======================================================================

filetype = 'JPG'

# ======================================================================
# Directories.
# ======================================================================

dirs = {
    'run 1' : '/home/kyle/beamtest_data/2016_07_18/',
    'run 2' : '/home/kyle/beamtest_data/2016_07_19/',
    'out' : '/home/kyle/beam_spot_code/output/',
    }

# ======================================================================
# Check if output directory exists. If it does not, make it.
# ======================================================================

def check_out_dir(dirs):
    if isinstance(dirs['out'], list):
        for key in dirs['out']:
            if not os.path.exists(dirs['out']):
                os.makedirs(dirs['out'])
    else:
        if not os.path.exists(dirs['out']):
            os.makedirs(dirs['out'])
    return 0

# ======================================================================
# Setup printing/output function.
# ======================================================================

def print_or_write(ofile):
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
    output = print_or_write(ofile)
    if path is None:
        output('File: {}\n'.format(fname))
        return imread(fname)
    else:
        output('File: {}\n\tPath: {}'.format(fname, path))
        return imread(path)

# ======================================================================
# Output statistics.
# ======================================================================

def stats(data, ofile=None, add_keys=None):
    output = print_or_write(ofile)
    if (add_keys is None):
        keys = moment_keys
    else:
        keys = moment_keys + add_keys
    for key in keys:
        if key in data:
            output('\t{}: {}'.format(key, data[key]))
    return None

# ======================================================================
# Measurement file finder.
# ======================================================================

def meas_file(run, serial):
    return glob.glob(
        '{}IMG_2016_07_1{}T??_??_??_SN_{:04}.{}'.format(
            dirs['run {}'.format(run)], run+7, serial, filetype,
            )
        )

# ======================================================================
# Measurement file (existance) checker (returns file list).
# ======================================================================

def check_meas_files():
    output = print_or_write(ofile)
    output('Checking/finding image files...')
    runs = []
    if not os.path.exists(dirs['run 1']):
        output(
            'Warning:\nThe measurement file directory for run 1('
            + dirs['run 1'] + ') does not exist.'
            )
    else:
        runs += [1]
    if not os.path.exists(dirs['run 2']):
        output(
            'Warning:\nThe measurement file directory for run 2('
            + dirs['run 2'] + ') does not exist.')
    else:
        runs += [2]
    num_found = 0
    errors = []
    found = {}
    for r in runs:
        found[r] = {}
        for k1 in data_files[r]:
            found[r][k1] = {}
            for k2 in data_files[r][k1]:
                found[r][k1][k2] = []
                for i in range(data_files[r][k1][k2].shape[0]):
                    sa = int(data_files[r][k1][k2][i, 1])
                    sb = int(data_files[r][k1][k2][i, 2]) + 1
                    for s in range(sa, sb):
                        path = meas_file(r, s)
                        num = len(path)
                        if (num != 1):
                            errors += [[r, k1, k2, sa, sb, s, path, num]]
                        else:
                            num_found += 1
                            found[r][k1][k2] += [[
                                # Approximate current in amperes.
                                data_files[r][k1][k2][i, 0],
                                # Serial number.
                                s,
                                # Path.
                                path[0],
                                ]]
    num_errors = len(errors)
    output(
        'Number of files found*:\t{}\nNumber of errors:      \t{}\n'.format(
            num_found, num_errors
            )
        + '*Excluding duplicates.'
        )
    if (num_errors > 0):
        output(
            '\nErrors:\nrun\tkey1\tkey2\tstart\tstop\tserial numumber\tnumber '
            + 'found')
        for i in range(num_errors):
            output(
                '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                    errors[i][0], errors[i][1], errors[i][2], errors[i][3],
                    errors[i][4], errors[i][5], errors[i][7]
                    )
                )
    return found

# ======================================================================
# Data file (photo) serial number listing.
# ======================================================================

data_files = {
    1 : {
        'grid' : {
            'room' : np.asarray([
                [0.000, 47, 48],
                ]),
            },
        'room' : {
            'main' : np.asarray([
                [0.000, 49, 51],
                [0.108, 52, 56],
                [0.206, 57, 61],
                [0.310, 62, 66],
                [0.403, 67, 72],
                [0.500, 73, 77],
                [0.610, 78, 82],
                [0.710, 83, 87],
                [0.803, 88, 92],
                [0.900, 92, 97],
                [1.000, 98, 102],
                [1.100, 103, 107],
                [1.372, 108, 110],
                ]),
            },
        'cryo' : {
             'main' : np.asarray([
                [0.000, 111, 115],
                [0.101, 116, 120],
                [0.200, 121, 128],
                [0.290, 129, 133],
                [0.443, 134, 138],
                [0.524, 139, 143],
                [0.687, 144, 148],
                [0.845, 149, 154],
                [1.060, 155, 158],
                [1.509, 159, 164],
                [2.011, 165, 169],
                [2.599, 170, 174],
                [3.028, 175, 179],
                [3.548, 180, 184],
                [4.095, 185, 189],
                [4.650, 191, 195],
                [4.966, 196, 200],
                ]),
            'trapped' : np.asarray([
                [0.000, 201, 205],
                ]),
            },
        },
    2 : {
        'grid' : {
            'room' : np.asarray([
                [np.nan, 214, 218],
                ]),
            'cryo' : np.asarray([
                [np.nan, 556, 564],
                ]),
            },
        'noise' : {
            'cryo' : np.asarray([
                [np.nan, 865, 870],
                ]),
            },
        'room' : {
            'pos main' : np.asarray([
                [0.000, 219, 224],
                [0.049, 225, 229],
                [0.132, 230, 234],
                [0.207, 235, 239],
                [0.384, 240, 244],
                [0.448, 245, 249],
                [0.577, 250, 254],  # eLog: SN 250-250.
                [0.748, 255, 259],
                [0.885, 260, 264],
                [0.958, 265, 269],
                [1.064, 270, 274],
                [1.169, 275, 279],
                [1.298, 280, 284],
                [1.378, 285, 289],
                [1.525, 290, 294],
                [1.627, 295, 299],
                [1.772, 300, 304],
                [1.875, 305, 309],
                [2.075, 310, 314],
                ]),
            'pos rand' : np.asarray([
                [1.000, 320, 324],
                [0.200, 325, 329],
                [0.300, 330, 334],
                [0.800, 335, 339],
                [0.100, 340, 349],
                [0.600, 345, 349],
                [1.300, 350, 354],
                [1.800, 355, 359],
                [1.900, 360, 364],
                [1.600, 365, 369],
                [1.401, 370, 374],
                [0.000, 375, 379],
                [0.700, 380, 384],
                [0.400, 385, 384],
                [1.500, 390, 394],
                [1.700, 395, 399],
                [1.200, 400, 404],
                [0.900, 405, 409],
                [1.999, 410, 414],
                [1.100, 415, 419],
                ]),
            'neg main' : np.asarray([
                [0.000, 422, 429],
                [-0.249, 430, 434],
                [-0.751, 440, 445],
                [-1.001, 446, 450],
                [-1.250, 451, 455],
                [-1.500, 456, 460],
                [-1.750, 461, 465],
                [-2.000, 466, 470],  # eLog: SN 466-465.
                [-2.250, 471, 475],
                [-2.502, 476, 480],
                ]),
            'neg to pos' : np.asarray([
                [-2.375, 481, 485],
                [-1.374, 486, 490],
                [-1.126, 491, 495],  # eLog: SN 491-195.
                [-0.875, 496, 500],
                [-0.625, 501, 505],
                [-0.375, 506, 510],
                [-0.126, 511, 515],
                [0.000, 516, 520],
                [0.257, 521, 525],
                [0.355, 526, 530],
                [0.499, 531, 535],
                [0.644, 536, 540],
                [0.769, 541, 545],
                [1.009, 546, 550],
                [1.338, 551, 555],
                ]),
            },
        'cryo' : {
            'neg main' : np.asarray([
                [0.000, 565, 569],
                [-0.052, 570, 574],
                [-0.142, 575, 579],
                [-0.269, 580, 584],
                [-0.339, 585, 589],
                [-0.479, 590, 594],
                [-0.575, 595, 599],
                [-0.622, 600, 604],
                [-0.718, 605, 609],
                [-0.846, 610, 614],
                [-0.958, 615, 619],
                [-1.100, 620, 624],
                [-1.242, 625, 629],
                [-1.411, 630, 634],
                [-1.643, 635, 639],
                [-1.935, 640, 644],
                [-2.271, 645, 649],
                [-2.458, 650, 654],
                [-2.901, 655, 659],
                [-3.111, 660, 664],
                [-3.340, 665, 669],
                [-3.510, 670, 674],
                [-3.838, 675, 679],
                [-4.125, 680, 684],
                [-4.478, 685, 689],
                [-4.756, 690, 694],
                [-5.184, 695, 699],
                ]),
            'neg to pos' : np.asarray([
                [-4.020, 700, 704],
                [-3.002, 705, 709],
                [-1.888, 710, 714],
                [-1.003, 715, 719],
                [-0.679, 720, 724],
                [-0.411, 725, 729],
                [-0.167, 730, 734],
                [0.000, 735, 739],
                [0.071, 740, 744],
                [0.271, 745, 749],
                [0.502, 750, 754],
                [0.791, 755, 759],
                [1.041, 760, 764],
                [1.169, 765, 769],
                [1.376, 770, 774],
                [1.791, 775, 779],
                [2.572, 780, 784],
                [3.071, 785, 789],
                [3.561, 790, 794],
                [4.220, 795, 799],
                [4.637, 800, 804],
                [4.819, 805, 809],
                [4.946, 810, 814],
                [5.213, 815, 819],
                ]),
            'pos to zero' : np.asarray([
                [4.500, 820, 824],
                [3.960, 825, 829],
                [3.308, 830, 834],
                [2.375, 835, 839],
                [1.591, 840, 844],
                [0.839, 845, 849],
                [0.386, 850, 854],
                [0.143, 855, 859],
                [0.000, 860, 864],
                ]),
            },
        },
    }

# ======================================================================
