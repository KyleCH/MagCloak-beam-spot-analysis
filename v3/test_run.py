#!/usr/bin/env python3

import beam_spot.processing as bsp

bsp.binary_hist('./test_image.png', use=['I', 'L', 'V'])
bsp.binary_hist('./IMG_0478.JPG', use=['I', 'L', 'V'])
bsp.binary_hist('./IMG_0479.JPG', use=['I', 'L', 'V'])
bsp.binary_hist('./IMG_0483.JPG', use=['I', 'L', 'V'])
bsp.binary_hist('./IMG_0487.JPG', use=['I', 'L', 'V'])
