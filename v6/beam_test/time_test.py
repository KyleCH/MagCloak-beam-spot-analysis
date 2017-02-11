#!/usr/bin/env python3

import timeit

import numpy as np

from beam_spot.colors_full import from_RGB_pixel_vect, from_RGB_wo_vect, from_RGB_w_vect
from beam_spot import modio

test_files = [
    './test_images/test_image.png',
    './test_images/test_image.png',
    './test_images/IMG_0478.JPG',
    './test_images/IMG_0479.JPG',
    './test_images/IMG_0483.JPG',
    './test_images/IMG_0487.JPG',
    ]

fns = [
    [from_RGB_pixel_vect, 'from_RGB_pixel_vect(img)'],
    [from_RGB_wo_vect, 'from_RGB_wo_vect(img)'],
    [from_RGB_w_vect, 'from_RGB_w_vect(img)'],
    ]

# modio.check_out_dir(dirs)

print('')

for fname in test_files:
    img = modio.image(fname)
    img = img.astype(np.int16)
    print('\nUsing {}...\n'.format(fname))
    for n in range(len(fns)):
        print(fns[n][1]+':')
        f = fns[n][0]
        print(
            timeit.repeat(
                'f(img)',
                setup='from __main__ import f, img',
                number=10,
                )
            )
#        t = timeit.Timer(
#            stmt='f(img)',
#            setup='from __main__ import f, img',
#            )
        
print('')
