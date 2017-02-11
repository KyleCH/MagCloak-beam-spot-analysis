#!/usr/bin/env python3

import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['figure.figsize'] = [8, 6]

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import uncertainties as unc

raw = np.load('./v12_b_results_2016-10-02_23-40-31.npy')[0]

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
# Average positions over current each value.
# ======================================================================

ofile.write(
    '='*80 + '\nAverage positions over current each value.\n' + '='*80 + '\n\n'
    )

data = {}

for k0 in raw:
    ofile.write('Run: {}\n'.format(k0))
    data[k0] = {}
    for k1 in raw[k0]:
        ofile.write('\tTemp: {}\n'.format(k1))
        data[k0][k1] = {}
        for k2 in raw[k0][k1]:
            ofile.write('\t\tType: {}\n'.format(k2))
            data[k0][k1][k2] = []
            I = raw[k0][k1][k2][0]['I']
            d = raw[k0][k1][k2][0]
            for n in range(1, raw[k0][k1][k2].shape[0]):
                if (raw[k0][k1][k2][n]['I'] == I):
                    d = np.append(d, raw[k0][k1][k2][n])
                else:
                    data[k0][k1][k2] += [
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
                    ofile.write('\t\t\t{}\n'.format(data[k0][k1][k2][-1]))
                    I = raw[k0][k1][k2][n]['I']
                    d = raw[k0][k1][k2][n]
            data[k0][k1][k2] += [
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
            data[k0][k1][k2] = np.array(
                data[k0][k1][k2],
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
            ofile.write('\t\t\t{}\n'.format(data[k0][k1][k2][-1]))

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

#-----------------------------------------------------------------------

ofile.write('\n')
r1 = unc.ufloat(popt[1]['room'], perr[1]['room'])*1e3
c1 = unc.ufloat(popt[1]['cryo'], perr[1]['cryo'])*1e3
r2 = unc.ufloat(popt[2]['room'], perr[2]['room'])*1e3
c2 = unc.ufloat(popt[2]['cryo'], perr[2]['cryo'])*1e3
ofile.write('r1: {:S}\n'.format(r1))
ofile.write('r2: {:S}\n'.format(r2))
ofile.write('c1: {:S}\n'.format(c1))
ofile.write('c2: {:S}\n'.format(c2))
ofile.write('r1/r2: {:S}\n'.format(r1/r2))
ofile.write('c1/c2: {:S}\n'.format(c1/c2))
s1 = 1 - c1 / r1
s2 = 1 - c2 / r2
ofile.write('s1: {:%S}\n'.format(s1))
ofile.write('s2: {:%S}\n'.format(s2))
ofile.write('(s1+s2)/2: {:%S}\n'.format((s1+s2)/2))
ofile.write('s1-s2: {:%S}\n'.format(s1-s2))
w1 = 1/s1.s**2
w2 = 1/s2.s**2
s = unc.ufloat((s1.n*w1+s2.n*w2)/(w1+w2), 1/np.sqrt(w1+w2))
ofile.write('s: {:%S}\n'.format(s))


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
fig.savefig('./raw_plot_Li.png')
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
fig.savefig('./raw_plot_O.png')
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
ax.set_ylim(-.05, 0.25)
#ax.legend(loc='best')
fig.savefig('./TUPOB43f3.png')
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
ax.set_ylim(-.25, .2)
#ax.legend(loc='best')
fig.savefig('./TUPOB43f4.png')
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
fig.savefig('./calc_plot_O_room.png')
plt.close()
'''
# ======================================================================
# Shielding analysis.
# ======================================================================

leakage = {}
shielding = {}
for k0 in [1, 2]:
    leakage[k0] = popt[k0]['cryo'] / popt[k0]['room']
    
    shielding[k0] = 1 - leakage[k0]
    

# ======================================================================

ofile.write('\n' + '='*80)

ofile.close()
