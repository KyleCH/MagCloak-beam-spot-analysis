# python3

from beam_spot import load_data
from beam_spot import processing as bsp

# ======================================================================

# Make sure output directory exists.
load_data.check_out_dir()

# Get measurement files.
files = load_data.check_meas_files()

# Loop over measurement files...
for run in files:
    for k1 in files[run]:
        for k2 in files[run][k1]:
            for n in range(len(files[run][k1][k2])):
                # Load file.
                #rgb = imread(files[run][k1][k2][n][3]
                # Convert color system.
                #img_c = colors.from_RGB_wo_vect(rgb)
                bsp.binary_hist(
                    files[run][k1][k2][n][2],
                    use=['I', 'L', 'V', 'Yp601', 'Yp709'],
                    odir=load_data.dirs['out'],
                    )

# ======================================================================
