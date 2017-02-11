#!/usr/bin/env python3

import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as scindi

# ======================================================================
# Parameters.
# ======================================================================

sigma = 51
low = 0.03 * 256
high = 255
roi = None

filetype = 'JPG'

# ======================================================================
# Directories.
# ======================================================================

dirs = {
    'run 1' : '/home/kyle/beam_test/raw_data/2016_07_18/',
    'run 2' : '/home/kyle/beam_test/raw_data/2016_07_19/',
    'out' : '/home/kyle/beam_test/output/gaussian_filter/',
    }

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
# Check if output directory exists. If it does not, make it.
# ======================================================================

def check_out_dir():
    if isinstance(dirs['out'], list):
        for key in dirs['out']:
            if not os.path.exists(dirs['out']):
                os.makedirs(dirs['out'])
    else:
        if not os.path.exists(dirs['out']):
            os.makedirs(dirs['out'])
    return 0

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
# Measurement file (existance) checker (returns file list).
# ======================================================================

def check_meas_files(ofile=None):
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
# Calculate moments.
# ======================================================================

def moments(w, low=0, high=255, roi=None):
    if (roi is None):
        roi = np.asarray(
            [
                [0, w.shape[0]],
                [0, w.shape[1]],
                ]
            )
    W = 0.
    m1 = np.zeros(2)
    m2 = np.zeros(2)
    z = np.empty(2)
    for y in range(roi[0, 0], roi[0, 1]):
        for x in range(roi[1, 0], roi[1, 1]):
            if ((w[y, x] >= low) or (w[y, x] <= high)):
                W += w[y, x]
                z[:] = w[y, x]
                z[:] *= [x, y]
                m1 += z
                z[:] *= [x, y]
                m2 += z
    m1 /= W
    m2 /= W
    m2 -= m1**2
    std = np.sqrt(m2)
    return np.asarray(
        [
            [m1[0], std[0]],
            [m1[1], std[1]],
            ]
        )

# ======================================================================
# Process data.
# ======================================================================

def process(fname, serial, sigma=51, low=0.03*256, high=255, roi=None):
    img = scindi.imread(fname)
#    img = img.astype(np.float16)
    img = img.mean(axis=2)
    img = scindi.gaussian_filter(img, sigma)
    stats = moments(img, low, high, roi)
    
    fig, ax = plt.subplots(1)
    ax.imshow(img, cmap='Greys_r')
    ax.errorbar(
        stats[0, 0], stats[1, 0],
        xerr=stats[0, 1], yerr=stats[1, 1],
        )
    ly, lx = img.shape
    ax.xaxis.tick_top()
    ax.set_xlim(-.5, lx-.5)
    ax.set_ylim(ly-.5, -.5)
    fig.savefig(dirs['out']+'{:04}.png'.format(serial))
    plt.close()
    
    return stats

# ======================================================================
# Run.
# ======================================================================

#if (__name__ == '__main__'):
print('Starting...')
check_out_dir()
with open(dirs['out']+'info.txt', 'w') as f:
    print('Running...')
    f.write(
        'Data Analysis Using Gaussian Filtering\n'
        + '\tsigma:\t{}\n\tlow:\t{}\n\thigh:\t{}'.format(
            sigma, low, high,
            )
        )
#        if (roi is not None):
#            f.write('\n\troi:\t[[{}, {}], [{}, {}]]'.format(
#                roi[0, 0],
#                roi[0, 1],
#                roi[1, 0],
#                roi[1, 1],
#                )
#            )
#        else:
#            f.write('\n\troi:\t{}'.format(roi))
    files = check_meas_files(f)
    f.write('\n\troi:\t{}'.format(roi))
    f.write(
            '\nRun\tType\tSet'
            + '\tCurrent\tSerial Num.'
            + '\tMean x\tStd. Dev. x'
            + '\tMean y\tStd. Dev. y'
            )
    for r in files:
        print('Run: {}'.format(r))
        for k1 in ['room', 'cryo']:
            print('\tType: {}'.format(k1))
            for k2 in files[r][k1]:
                print('\t\tSet: {}'.format(k2))
                for n in range(len(files[r][k1][k2])):
                    print('\t\t\tSerial: {}'.format(files[r][k1][k2][n][1]))
                    stats = process(
                        files[r][k1][k2][n][2],
                        files[r][k1][k2][n][1],
                        sigma,
                        low,
                        high,
                        roi,
                        )
                    f.write(
                        '\n{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                            r,
                            k1,
                            k2,
                            files[r][k1][k2][n][0],
                            files[r][k1][k2][n][1],
                            stats[0, 0],
                            stats[0, 1],
                            stats[1, 0],
                            stats[1, 1],
                            )
                        )
                    print(
                        '\t\t\t\tx: {}, {}\n\t\t\t\ty: {}, {}'.format(
                            stats[0, 0], stats[0, 1],
                            stats[1, 0], stats[1, 1],
                            )
                        )
print('Done.')
