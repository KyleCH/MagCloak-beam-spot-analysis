#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import uncertainties as unc

# ======================================================================
# Parameters.
# ======================================================================

ifname = './v12_b_results_2016-10-02_23-40-31.npy'
ofname = './v12_c_results.txt'
ofile = open(ofname, 'w')

colors = {
    'room' : '#ff0000',
    'cryo' : '#0000ff',
    'trapped' : '#00ff00',
    }

current_to_field = 8.0
pixel_to_distnce = 0.003/2

# ======================================================================
# Functions.
# ======================================================================

# ----------------------------------------------------------------------
# Label.
# ----------------------------------------------------------------------

def label(lbl, ofile, last=False):
    ofile.write('='*80 + '\n{}\n'.format(lbl) + '='*80 + '\n'*2)
    return None

# ----------------------------------------------------------------------
# Loop over.
# ----------------------------------------------------------------------

def loop(d, f, *args, levels=4, ofile=None, result=True, **kwargs):
    # Return results.
    if result:
        r = {}
        # Don't output to file.
        if (ofile is None):
            if (levels == 4):
                for k0 in d:
                    r[k0] = {}
                    for k1 in d[k0]:
                        r[k0][k1] = {}
                        for k2 in d[k0][k1]:
                            r[k0][k1][k2] = []
                            for n in range(d[k0][k1][k2].shape[0]):
                                r[k0][k1][k2] += f(*args, **kwargs)
            elif (levels == 3):
                for k0 in d:
                    r[k0] = {}
                    for k1 in d[k0]:
                        r[k0][k1] = {}
                        for k2 in d[k0][k1]:
                            r[k0][k1][k2] = f(*args, **kwargs)
            elif (levels == 2):
                for k0 in d:
                    r[k0] = {}
                    for k1 in d[k0]:
                        r[k0][k1] = f(*args, **kwargs)
            elif (levels == 1):
                for k0 in d:
                    r[k0] = f(*args, **kwargs)
            else:
                pass
        # Output to file.
        else:
            if (levels == 4):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    r[k0] = {}
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        r[k0][k1] = {}
                        for k2 in d[k0][k1]:
                            ofile.write('\t\tk2: {}\n'.format(k2))
                            r[k0][k1][k2] = []
                            for n in range(d[k0][k1][k2].shape[0]):
                                r[k0][k1][k2] += f(
                                    *args, ofile=ofile, **kwargs)
            elif (levels == 3):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    r[k0] = {}
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        r[k0][k1] = {}
                        for k2 in d[k0][k1]:
                            ofile.write('\t\tk2: {}\n'.format(k2))
                            r[k0][k1][k2] = f(*args, ofile=ofile, **kwargs)
            elif (levels == 2):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    r[k0] = {}
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        r[k0][k1] = f(*args, ofile=ofile, **kwargs)
            elif (levels == 1):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    r[k0] = f(*args, ofile=ofile, **kwargs)
            else:
                pass
    # Don't return results.
    else:
        # Don't output to file.
        if (ofile is None):
            if (levels == 4):
                for k0 in d:
                    for k1 in d[k0]:
                        for k2 in d[k0][k1]:
                            for n in range(d[k0][k1][k2].shape[0]):
                                f(*args, **kwargs)
            elif (levels == 3):
                for k0 in d:
                    for k1 in d[k0]:
                        for k2 in d[k0][k1]:
                            f(*args, **kwargs)
            elif (levels == 2):
                for k0 in d:
                    for k1 in d[k0]:
                        f(*args, **kwargs)
            elif (levels == 1):
                for k0 in d:
                    f(*args, **kwargs)
            else:
                pass
        # Output to file.
        else:
            if (levels == 4):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        for k2 in d[k0][k1]:
                            ofile.write('\t\tk2: {}\n'.format(k2))
                            for n in range(d[k0][k1][k2].shape[0]):
                                f(*args, ofile=ofile, **kwargs)
            elif (levels == 3):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        for k2 in d[k0][k1]:
                            ofile.write('\t\tk2: {}\n'.format(k2))
                            f(*args, ofile=ofile, **kwargs)
            elif (levels == 2):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    for k1 in d[k0]:
                        ofile.write('\tk1: {}\n'.format(k1))
                        f(*args, ofile=ofile, **kwargs)
            elif (levels == 1):
                for k0 in d:
                    ofile.write('k0: {}\n'.format(k0))
                    f(*args, ofile=ofile, **kwargs)
            else:
                pass
    return None

# ----------------------------------------------------------------------
# Calculate position statistics for measurements with the same current.
# ----------------------------------------------------------------------

def average(raw):
    data = []
    d = raw[0]
    I = d['I']
    for n in range(1, raw.shape[0]):
        if (raw[n]['I'] == I):
            d = np.append(d, raw[n])
        else:
            data += [
                (
                    I*current_to_field,
                    d['SN'].min()*pixel_to_distnce,
                    d['SN'].max()*pixel_to_distnce,
                    d['x'].mean()*pixel_to_distnce,
                    d['x'].std()*pixel_to_distnce,
                    d['y'].mean()*pixel_to_distnce,
                    d['y'].std()*pixel_to_distnce,
                    ),
                ]
            ofile.write('\t\t\t{}\n'.format(data[-1]))
            d = raw[0]
            I = d['I']
    data += [
        (
            I*current_to_field,
            d['SN'].min()*pixel_to_distnce,
            d['SN'].max()*pixel_to_distnce,
            d['x'].mean()*pixel_to_distnce,
            d['x'].std()*pixel_to_distnce,
            d['y'].mean()*pixel_to_distnce,
            d['y'].std()*pixel_to_distnce,
            ),
        ]
    data = np.array(
        data,
        dtype=[
            ('I', 'f4'),
            ('start', 'i2'),
            ('stop', 'i2'),
            ('x', 'f4'),
            ('sx', 'f4'),
            ('y', 'f4'),
            ('sy', 'f4'),
            ],
        )
    ofile.write('\t\t\t{}\n'.format(data[-1]))
    return data

# ----------------------------------------------------------------------
# Fitter.
# ----------------------------------------------------------------------

def fitter(x, y, sigma, p0=[100], fitline_x=[-50, 50]):
    popt, pcov = opt.curve_fit(f, x, y, p0, sigma, True)
    perr = np.sqrt(np.diag(pcov))
    fx = f(x, *popt)
    res = (y-fx) / sigma
    chisq = np.sum(res**2)
    return {
        'popt' : unp.uarray(popt, perr),
        'pcov' : pcov,
        'fx' : fx,
        'fitline' : np.array([fitline_x, f(fitline_x, *popt)]),
        'res' : res,
        'chisq' : chisq,
        'redchisq' : chisq / (len(res)-len(popt)-1),
        }

# ----------------------------------------------------------------------

# ======================================================================
# Load raw data and open output file.
# ======================================================================

raw = np.load(ifname)[0]

# ======================================================================
# Average positions over current each value.
# ======================================================================

ofile.write(
    '='*80 + '\n'
    + 'Average positions over current each value.' + '\n'
    + '='*80 + '\n'*2
    )

data = loop(raw, average, levels=3, ofile=ofile, result=True)

# ======================================================================
# Convert positions to displacements.
# ======================================================================

ofile.write(
    '\n' + '='*80 + '\nConvet positions to displacements.\n' + '='*80 + '\n\n'
    )

k0 = 1
k1 = 'room'
k2 = 'main'
n0 = 0
ofile.write('{}, {}, {}: {}\n'.format(k0, k1, k2, data[k0][k1][k2][n0]['I']))
x0 = data[k0][k1][k2]['x'][n0]
sx0 = data[k0][k1][k2]['sx'][n0]
y0 = data[k0][k1][k2]['y'][n0]
sy0 = data[k0][k1][k2]['sy'][n0]
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
data[k0][k1][k2]['sx'][n0] = 0
data[k0][k1][k2]['sy'][n0] = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'cryo'
n0 = 0
ofile.write('{}, {}, {}: {}\n'.format(k0, k1, k2, data[k0][k1][k2][n0]['I']))
x0 = data[k0][k1][k2]['x'][n0]
sx0 = data[k0][k1][k2]['sx'][n0]
y0 = data[k0][k1][k2]['y'][n0]
sy0 = data[k0][k1][k2]['sy'][n0]
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
data[k0][k1][k2]['sx'][n0] = 0
data[k0][k1][k2]['sy'][n0] = 0
k2 = 'trapped'
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)

# ----------------------------------------------------------------------

k0 = 2
k1 = 'room'
k2 = 'pos main'
n0 = 0
ofile.write('{}, {}, {}: {}\n'.format(k0, k1, k2, data[k0][k1][k2][n0]['I']))
x0 = data[k0][k1][k2]['x'][n0]
sx0 = data[k0][k1][k2]['sx'][n0]
y0 = data[k0][k1][k2]['y'][n0]
sy0 = data[k0][k1][k2]['sy'][n0]
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
data[k0][k1][k2]['sx'][n0] = 0
data[k0][k1][k2]['sy'][n0] = 0
k2 = 'pos rand'
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)

k1 = 'room'
k2 = 'neg main'
n0 = 0
ofile.write('{}, {}, {}: {}\n'.format(k0, k1, k2, data[k0][k1][k2][n0]['I']))
x0 = data[k0][k1][k2]['x'][n0]
sx0 = data[k0][k1][k2]['sx'][n0]
y0 = data[k0][k1][k2]['y'][n0]
sy0 = data[k0][k1][k2]['sy'][n0]
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
k2 = 'neg to pos'
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'cryo'
k2 = 'neg main'
n0 = 0
ofile.write('{}, {}, {}: {}\n'.format(k0, k1, k2, data[k0][k1][k2][n0]['I']))
x0 = data[k0][k1][k2]['x'][n0]
sx0 = data[k0][k1][k2]['sx'][n0]
y0 = data[k0][k1][k2]['y'][n0]
sy0 = data[k0][k1][k2]['sy'][n0]
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
data[k0][k1][k2]['sx'][n0] = 0
data[k0][k1][k2]['sy'][n0] = 0
k2 = 'neg to pos'
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)
k2 = 'pos to zero'
data[k0][k1][k2]['x'] -= x0
data[k0][k1][k2]['sx'] = np.sqrt(data[k0][k1][k2]['sx']**2 + sx0**2)
data[k0][k1][k2]['y'] -= y0
data[k0][k1][k2]['sy'] = np.sqrt(data[k0][k1][k2]['sy']**2 + sy0**2)

# ======================================================================
# Print indices.
# ======================================================================

#ofile.write('\n' + '='*80 + '\nPrint indices.\n' + '='*80 + '\n\n')
#for k0 in data:
#    ofile.write('k0:', k0)
#    for k1 in data[k0]:
#        ofile.write('    k1:', k1)
#        for k2 in data[k0][k1]:
#            ofile.write('        k2:', k2)
#            for n, I in enumerate(data[k0][k1][k2]['I']):
#                ofile.write('            {}: {}'.format(n, I))

# ======================================================================
# Print data (now that positions have been converted to displacements).
# ======================================================================

ofile.write('\n' + '='*80 + '\nData (displacements).\n' + '='*80 + '\n\n')

for k0 in data:
    ofile.write('k0: {}\n'.format(k0))
    for k1 in data[k0]:
        ofile.write('\tk1: {}\n'.format(k1))
        for k2 in data[k0][k1]:
            ofile.write('\t\tk2: {}\n'.format(k2))
            for n in range(data[k0][k1][k2].shape[0]):
                ofile.write(
                    '\t\t\t{},  # n={}.\n'.format(
                        data[k0][k1][k2][n],
                        n,
                        )
                    )
#                ofile.write(
#                    '\t\t\t{} {} {} {} {} {} {}  # n={}.\n'.format(
#                        data[k0][k1][k2][n]['I'],
#                        data[k0][k1][k2][n]['start'],
#                        data[k0][k1][k2][n]['stop'],
#                        data[k0][k1][k2][n]['x'],
#                        data[k0][k1][k2][n]['sx'],
#                        data[k0][k1][k2][n]['y'],
#                        data[k0][k1][k2][n]['sy'],
#                        n,
#                        )
#                    )

# ======================================================================
# Fitting.
# ======================================================================

ofile.write('\n' + '='*80 + '\nFitting.\n' + '='*80 + '\n\n')

def f(x, m, b=0):
    return m*x + b

popt = {
    1 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    2 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    }
pcov = {
    1 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    2 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    }
perr = {
    1 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    2 : {
        'room' : np.nan,
        'cryo' : np.nan,
        },
    }
fit = {
    1 : {
        'room' : {},
        'cryo' : {},
        },
    2 : {
        'room' : {},
        'cryo' : {},
        },
    }

# ----------------------------------------------------------------------

k0 = 1
k2 = 'main'
ofile.write('Run 1:\n')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'room'
ofile.write('\tRoom:\n')
popt[k0][k1], pcov[k0][k1] = opt.curve_fit(
    f,
    data[k0][k1][k2]['I'][1:7],
    data[k0][k1][k2]['x'][1:7],
#    p0=[100, 0],
    p0=[100],
    sigma=data[k0][k1][k2]['sx'][1:7],
    absolute_sigma=True,
    )
perr[k0][k1] = np.sqrt(np.diag(pcov[k0][k1]))
fit[k0][k1]['y'] = f(data[k0][k1][k2]['I'], *popt[k0][k1])
fit[k0][k1]['r'] = (
    (data[k0][k1][k2]['x'][1:7]-fit[k0][k1]['y'][1:7])
    / data[k0][k1][k2]['sx'][1:7]
    )
fit[k0][k1]['chi square'] = np.sum(fit[k0][k1]['r']**2)
fit[k0][k1]['reduced chi square'] = fit[k0][k1]['chi square'] / (
    len(fit[k0][k1]['r'])-len(popt[k0][k1])-1
    )
ofile.write('\t\tpopt: {}\n'.format(popt[k0][k1]))
ofile.write('\t\tperr: {}\n'.format(perr[k0][k1]))
ofile.write('\t\tChi Square: {}\n'.format(fit[k0][k1]['chi square']))
ofile.write(
    '\t\tReduced Chi Square: {}\n'.format(fit[k0][k1]['reduced chi square'])
    )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'cryo'
ofile.write('\tCryo:\n')
popt[k0][k1], pcov[k0][k1] = opt.curve_fit(
    f,
    data[k0][k1][k2]['I'][1:],
    data[k0][k1][k2]['x'][1:],
#    p0=[100, 0],
    p0=[100],
    sigma=data[k0][k1][k2]['sx'][1:],
    absolute_sigma=True,
    )
perr[k0][k1] = np.sqrt(np.diag(pcov[k0][k1]))
fit[k0][k1]['y'] = f(data[k0][k1][k2]['I'], *popt[k0][k1])
fit[k0][k1]['r'] = (
    (data[k0][k1][k2]['x'][1:]-fit[k0][k1]['y'][1:])
    / data[k0][k1][k2]['sx'][1:]
    )
fit[k0][k1]['chi square'] = np.sum(fit[k0][k1]['r']**2)
fit[k0][k1]['reduced chi square'] = fit[k0][k1]['chi square'] / (
    len(fit[k0][k1]['r'])-len(popt[k0][k1])-1
    )
ofile.write('\t\tpopt: {}\n'.format(popt[k0][k1]))
ofile.write('\t\tperr: {}\n'.format(perr[k0][k1]))
ofile.write('\t\tChi Square: {}\n'.format(fit[k0][k1]['chi square']))
ofile.write(
    '\t\tReduced Chi Square: {}\n'.format(fit[k0][k1]['reduced chi square'])
    )

# ----------------------------------------------------------------------

k0 = 2
k2 = 'neg main'
ofile.write('Run 2:\n')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'room'
ofile.write('\tRoom:\n')
k21 = 'pos main'
k20 = 'main'
data[k0][k1][k20] = {}
data[k0][k1][k20]['I'] = np.append(
    data[k0][k1][k21]['I'][-1::-1],
    data[k0][k1][k2]['I'],
    )
data[k0][k1][k20]['x'] = np.append(
    data[k0][k1][k21]['x'][-1::-1],
    data[k0][k1][k2]['x'],
    )
data[k0][k1][k20]['sx'] = np.append(
    data[k0][k1][k21]['sx'][-1::-1],
    data[k0][k1][k2]['sx'],
    )
data[k0][k1][k20]['II'] = np.append(
    data[k0][k1][k21]['I'][8:0:-1],
    data[k0][k1][k2]['I'][1:4],
    )
data[k0][k1][k20]['xx'] = np.append(
    data[k0][k1][k21]['x'][8:0:-1],
    data[k0][k1][k2]['x'][1:4],
    )
data[k0][k1][k20]['sxx'] = np.append(
    data[k0][k1][k21]['sx'][8:0:-1],
    data[k0][k1][k2]['sx'][1:4],
    )
data[k0][k1][k20]['III'] = np.append(
    data[k0][k1][k21]['I'][-1:9:-1],
    data[k0][k1][k2]['I'][4:],
    )
data[k0][k1][k20]['xxx'] = np.append(
    data[k0][k1][k21]['x'][-1:9:-1],
    data[k0][k1][k2]['x'][4:],
    )
data[k0][k1][k20]['sxxx'] = np.append(
    data[k0][k1][k21]['sx'][-1:9:-1],
    data[k0][k1][k2]['sx'][4:],
    )
popt[k0][k1], pcov[k0][k1] = opt.curve_fit(
    f,
    data[k0][k1][k20]['II'],
    data[k0][k1][k20]['xx'],
#    p0=[100, 0],
    p0=[100],
    sigma=data[k0][k1][k20]['sxx'],
    absolute_sigma=True,
    )
perr[k0][k1] = np.sqrt(np.diag(pcov[k0][k1]))
fit[k0][k1]['y'] = f(data[k0][k1][k20]['I'], *popt[k0][k1])
fit[k0][k1]['yy'] = f(data[k0][k1][k20]['II'], *popt[k0][k1])
fit[k0][k1]['r'] = (
    (data[k0][k1][k20]['xx']-fit[k0][k1]['yy'])
    / data[k0][k1][k20]['sxx']
    )
fit[k0][k1]['chi square'] = np.sum(fit[k0][k1]['r']**2)
fit[k0][k1]['reduced chi square'] = fit[k0][k1]['chi square'] / (
    len(fit[k0][k1]['r'])-len(popt[k0][k1])-1
    )
ofile.write('\t\tpopt: {}\n'.format(popt[k0][k1]))
ofile.write('\t\tperr: {}\n'.format(perr[k0][k1]))
ofile.write('\t\tChi Square: {}\n'.format(fit[k0][k1]['chi square']))
ofile.write(
    '\t\tReduced Chi Square: {}\n'.format(fit[k0][k1]['reduced chi square'])
    )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

k1 = 'cryo'
ofile.write('\tCryo:\n')
popt[k0][k1], pcov[k0][k1] = opt.curve_fit(
    f,
    data[k0][k1][k2]['I'][1:],
    data[k0][k1][k2]['x'][1:],
#    p0=[100, 0],
    p0=[10],
    sigma=data[k0][k1][k2]['sx'][1:],
    absolute_sigma=True,
    )
perr[k0][k1] = np.sqrt(np.diag(pcov[k0][k1]))
fit[k0][k1]['y'] = f(data[k0][k1][k2]['I'], *popt[k0][k1])
fit[k0][k1]['r'] = (
    (data[k0][k1][k2]['x'][1:]-fit[k0][k1]['y'][1:])
    / data[k0][k1][k2]['sx'][1:]
    )
fit[k0][k1]['chi square'] = np.sum(fit[k0][k1]['r']**2)
fit[k0][k1]['reduced chi square'] = fit[k0][k1]['chi square'] / (
    len(fit[k0][k1]['r'])-len(popt[k0][k1])-1
    )
ofile.write('\t\tpopt: {}\n'.format(popt[k0][k1]))
ofile.write('\t\tperr: {}\n'.format(perr[k0][k1]))
ofile.write('\t\tChi Square: {}\n'.format(fit[k0][k1]['chi square']))
ofile.write(
    '\t\tReduced Chi Square: {}\n'.format(fit[k0][k1]['reduced chi square'])
    )

# ======================================================================
# Plotting.
# ======================================================================

ofile.write('\n' + '='*80 + '\nPlotting.\n' + '='*80 + '\n\n')

# ======================================================================
'''
fig, ax = plt.subplots(1)
ax.set_title('')
ax.set_xlabel('Current [A]')
ax.set_ylabel('Beam Spot Displacement [pixels]')
ax.errorbar(
    raw[1]['room']['main']['I'],
    raw[1]['room']['main']['x'],
    yerr=raw[1]['room']['main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='o',
    linestyle='',
    label='Room Temp.',
    )
ax.errorbar(
    raw[1]['cryo']['main']['I'],
    raw[1]['cryo']['main']['x'],
    yerr=raw[1]['cryo']['main']['sx'],
    ecolor=colors['cryo'],
    color=colors['cryo'],
    fmt='o',
    linestyle='',
    label='Cryogenic',
    )
ax.legend(loc='best')
fig.savefig('./raw_plot_Li.png', dpi=300)
plt.close()
'''
# ======================================================================
'''
fig, ax = plt.subplots(1)
ax.set_title('')
ax.set_xlabel('Current [A]')
ax.set_ylabel('Beam Spot Displacement [pixels]')
ax.errorbar(
    raw[2]['room']['neg main']['I'],
    raw[2]['room']['neg main']['x'],
    yerr=raw[2]['room']['neg main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='o',
    linestyle='',
    label='Room Temp.',
    )
ax.errorbar(
    raw[2]['room']['pos main']['I'],
    raw[2]['room']['pos main']['x'],
    yerr=raw[2]['room']['pos main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='o',
    linestyle='',
#    label='Room Temp.',
    )
ax.errorbar(
    raw[2]['cryo']['neg main']['I'],
    raw[2]['cryo']['neg main']['x'],
    yerr=raw[2]['cryo']['neg main']['sx'],
    ecolor=colors['cryo'],
    color=colors['cryo'],
    fmt='o',
    linestyle='',
    label='Cryogenic',
    )
ax.legend(loc='best')
fig.savefig('./raw_plot_O.png', dpi=300)
plt.close()
'''
# ======================================================================

fig, ax = plt.subplots(1)
ax.set_title('')
ax.set_xlabel('Applied Magnetic Field [mT]')
ax.set_ylabel('Beam Spot Displacement [mm]')
ax.plot(
    data[1]['room']['main']['I'],
    fit[1]['room']['y'],
    color=colors['room'],
    marker='',
    linestyle='-',
    label='Room Temp. Fit',
    )
ax.plot(
    data[1]['cryo']['main']['I'],
    fit[1]['cryo']['y'],
    color=colors['cryo'],
    marker='',
    linestyle='-',
    label='Cryogenic Fit',
    )
ax.errorbar(
    data[1]['room']['main']['I'][1:7],
    data[1]['room']['main']['x'][1:7],
    yerr=data[1]['room']['main']['sx'][1:7],
    ecolor='k',
    color=colors['room'],
    fmt='o',
    linestyle='',
    label='Fitted Room Temp.',
    )
ax.errorbar(
    data[1]['room']['main']['I'][7:],
    data[1]['room']['main']['x'][7:],
    yerr=data[1]['room']['main']['sx'][7:],
    ecolor='k',
    color=colors['room'],
    fmt='D',
    linestyle='',
    label='Excluded Room Temp.',
    )
ax.errorbar(
    data[1]['cryo']['main']['I'][1:],
    data[1]['cryo']['main']['x'][1:],
    yerr=data[1]['cryo']['main']['sx'][1:],
    ecolor='k',
    color=colors['cryo'],
    fmt='o',
    linestyle='',
    label='Fitted Cryogenic',
    )
ax.set_xlim(-5, 45)
ax.set_ylim(-.05, 0.4)
#ax.legend(loc='best')
fig.savefig('./calc_plot_Li.png', dpi=300)
plt.close()

# ======================================================================

fig, ax = plt.subplots(1)
ax.set_title('')
ax.set_xlabel('Applied Magnetic Field [mT]')
ax.set_ylabel('Beam Spot Displacement [mm]')
ax.plot(
    data[2]['room']['main']['I'],
    fit[2]['room']['y'],
    color=colors['room'],
    marker='',
    linestyle='-',
    label='Room Temp. Fit',
    )
ax.plot(
    data[2]['cryo']['neg main']['I'],
    fit[2]['cryo']['y'],
    color=colors['cryo'],
    marker='',
    linestyle='-',
    label='Cryogenic Fit',
    )
ax.errorbar(
    data[2]['room']['main']['II'],
    data[2]['room']['main']['xx'],
    yerr=data[2]['room']['main']['sxx'],
    ecolor='k',
    color=colors['room'],
    fmt='o',
    linestyle='',
    label='Room Temp.',
    )
ax.errorbar(
    data[2]['room']['main']['III'],
    data[2]['room']['main']['xxx'],
    yerr=data[2]['room']['main']['sxxx'],
    ecolor='k',
    color=colors['room'],
    fmt='D',
    linestyle='',
    label='Room Temp.',
    )
ax.errorbar(
    data[2]['cryo']['neg main']['I'][1:],
    data[2]['cryo']['neg main']['x'][1:],
    yerr=data[2]['cryo']['neg main']['sx'][1:],
    ecolor='k',
    color=colors['cryo'],
    fmt='o',
    linestyle='',
    label='Cryogenic',
    )
ax.set_xlim(-45, 20)
ax.set_ylim(-.45, .4)
#ax.legend(loc='best')
fig.savefig('./calc_plot_O.png', dpi=300)
plt.close()

# ======================================================================
'''
fig, ax = plt.subplots(1)
ax.set_title('')
ax.set_xlabel('Current [A]')
ax.set_ylabel('Beam Spot Displacement [pixels]')
ax.errorbar(
    data[2]['room']['pos main']['I'],
    data[2]['room']['pos main']['x'],
    yerr=data[2]['room']['pos main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='o',
    linestyle='-',
#    label='Room Temp.',
    )
ax.errorbar(
    data[2]['room']['pos rand']['I'],
    data[2]['room']['pos rand']['x'],
    yerr=data[2]['room']['pos main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='.',
    linestyle='-',
#    label='Room Temp.',
    )
ax.errorbar(
    data[2]['room']['neg main']['I'],
    data[2]['room']['neg main']['x'],
    yerr=data[2]['room']['neg main']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='+',
    linestyle='-',
    label='Room Temp.',
    )
ax.errorbar(
    data[2]['room']['neg to pos']['I'],
    data[2]['room']['neg to pos']['x'],
    yerr=data[2]['room']['neg to pos']['sx'],
    ecolor=colors['room'],
    color=colors['room'],
    fmt='x',
    linestyle='-',
#    label='Room Temp.',
    )
fig.savefig('./calc_plot_O_room.png', dpi=300)
plt.close()
'''
# ======================================================================
# Shielding analysis.
# ======================================================================

leakage = {}
for k0 in [1, 2]:
    leakage[k0] = popt[k0]['cryo'] / popt[k0]['room']
    
    shielding[k0] = 1 - leakage[k0]
    

# ======================================================================

ofile.write('\n' + '='*80)

ofile.close()
