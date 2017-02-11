#!/usr/bin/env python3

import numpy as np

# ======================================================================
# IFD entry tag types.
# ======================================================================

tag_type = {
    1 : chr,
    2 : str,
    3 : 'unsigned short (2 bytes)',
    4 : 'unsigned long (4 bytes)',
    5 : 'unsigned rationnal (2 unsigned long)',
    6 : 'signed char',
    7 : 'byte sequence',
    8 : 'signed short',
    9 : 'signed long',
    10 : 'signed rationnal (2 signed long)',
    11 : 'float, 4 bytes, IEEE format',
    12 : 'float, 8 bytes, IEEE format',
    }

tag_type_str = {
    1 : 'unsigned char',
    2 : 'string (with an ending zero)',
    3 : 'unsigned short (2 bytes)',
    4 : 'unsigned long (4 bytes)',
    5 : 'unsigned rationnal (2 unsigned long)',
    6 : 'signed char',
    7 : 'byte sequence',
    8 : 'signed short',
    9 : 'signed long',
    10 : 'signed rationnal (2 signed long)',
    11 : 'float, 4 bytes, IEEE format',
    12 : 'float, 8 bytes, IEEE format',
    }

# ======================================================================
# IFD #0.
# ======================================================================

# IFD #0 tags.
ifd0_tags = {
    0x0100 : ,
    0x0101 : ,
    0x0102 : ,
    0x0103 : ,
    0x010f : ,
    0x0110 : ,
    0x0111 : ,
    0x0112 : ,
    0x0117 : ,
    0x011a : ,
    0x011b : ,
    0x0128 : ,
    0x0132 : ,
    0x8769 : ,
    0x8825 : ,
    }

# EXIF tags.
exif_tags = {
    0x829a : ,
    0x829d : ,
    0x927c : ,
    }

# Makernote.

makernote = {
    0x0001 : ,
    0x0002 : ,
    0x0006 : ,
    0x0097 : ,
    0x00e0 : ,
    0x4001 : ,
    0x4002 : ,
    0x4003 : ,
    0x4004 : ,
    0x4005 : ,
    0x4006 : ,
    0x4007 : ,
    0x4008 : ,
    0x4009 : ,
    0x4010 : ,
    0x4011 : ,
    0x4012 : ,
    0x4013 : ,
    0x4014 : ,
    0x4015 : ,
    0x4016 : ,
    0x4017 : ,
    0x4018 : ,
    0x4019 : ,
    }


    }




