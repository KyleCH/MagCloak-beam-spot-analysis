#!/usr/bin/env python3

import datetime
import glob
import os

import numpy as np
#import scipy.ndimage as scindi

import datafiles

# ======================================================================
# Setup output directory.
# ======================================================================

def out_dir_setup(dirs):
    dirs['out'] += datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S/')
    if not os.path.exists(dirs['out']):
        os.makedirs(dirs['out'])
    return dirs

# ======================================================================
# Measurement file finder.
# ======================================================================

def meas_file(dirs, run, serial, filetype='JPG'):
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

def check_meas_files(dirs, files, ofile=None):
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
        for k1 in files[r]:
            found[r][k1] = {}
            for k2 in files[r][k1]:
                found[r][k1][k2] = []
                for i in range(files[r][k1][k2].shape[0]):
                    sa = int(files[r][k1][k2][i, 1])
                    sb = int(files[r][k1][k2][i, 2]) + 1
                    for s in range(sa, sb):
                        path = meas_file(dirs, r, s)
                        num = len(path)
                        if (num != 1):
                            errors += [[r, k1, k2, sa, sb, s, path, num]]
                        else:
                            num_found += 1
                            found[r][k1][k2] += [[
                                # Approximate current in amperes.
                                files[r][k1][k2][i, 0],
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
# Run.
# ======================================================================

def run(process, params, test=True):
    print('Starting...')
    dirs = out_dir_setup(datafiles.dirs)
    with open(dirs['out']+'info.txt', 'w') as f:
        print('Running...')
        if test:
            f.write('Data Analysis Test Run')
        else:
            f.write('Data Analysis Run')
        for pk in sorted(params.keys()):
            f.write('\n\t{}:\t{}'.format(pk, params[pk]))
        f.write('\n')
        if test:
            files = check_meas_files(dirs, datafiles.test_data_files, f)
        else:
            files = check_meas_files(dirs, datafiles.data_files, f)
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
                        print(
                            '\t\t\tSerial: {}'.format(files[r][k1][k2][n][1])
                            )
                        stats = process(
                            dirs=dirs,
                            fname=files[r][k1][k2][n][2],
                            serial=files[r][k1][k2][n][1],
                            current=files[r][k1][k2][n][0],
                            params=params,
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
    return 0

# ======================================================================
