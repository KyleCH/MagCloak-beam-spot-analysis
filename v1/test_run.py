#!/usr/bin/env python3

from beam_spot_analysis.load_data import image

#fig, ax = image('./IMG_0479.JPG')
fig, ax = image('./test_image.png')
#fig, ax = image('./test_image.jpg')
#fig, ax = image('./test_image.tiff')

fig.show()
input('Pause.')
