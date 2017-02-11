#!/usr/bin/env python3

from beam_spot import modio
from beam_spot import processing as bsp

# ======================================================================

# Make sure output directory exists.
modio.check_out_dir()

# Get measurement files.
files = modio.check_meas_files()

# Loop over measurement files...
for run in files:
    for k1 in files[run]:
        for k2 in files[run][k1]:
            for n in range(len(files[run][k1][k2])):
                bsp.binary_hist(
                    files[run][k1][k2][n][2],
                    use=['I', 'L', 'V', 'Yp601', 'Yp709'],
                    odir=load_data.dirs['out'],
                    )

# ======================================================================
