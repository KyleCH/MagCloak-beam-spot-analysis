#!/usr/bin/env python3

import numpy as np

# np.apply_along_axis(func1d, axis=2, arr)

# Zero chroma convention.
# np.nan : Hue is undefined.
# 0. : Hue is zero.
chroma_zero = 0.

# Hue scale.
# 360. / 6.=60. : Hue in degrees [0, 360).
# np.pi / 6. : Hue in radians [0, $\pi$).
# 1. / 6. : Hue range of [0, 1).
# 256. / 6. : Hue range of [0, 256).
hue_scale = 256. / 6.

scale = 256.

# Constant for calculation of beta.
half_rt_3 = np.sqrt(3.) / 2.

# ======================================================================
# Convert a single pixel from RGB (and vectorization for images).
# ======================================================================

def from_RGB_pixel(pixel):
    
    # Maximum.
    M = pixel.max()
    # Minimum.
    m = pixel.min()
    # Chroma.
#    C = M - m
    # Hue.
#    H = hue(pixel, C, M)
    
    # Alpha.
#    alpha = pixel[0] - .5*(pixel[1] + pixel[2])
    # Beta.
#    beta = half_rt_3 * (pixel[1] - pixel[2])
    # Hue 2 (hexagonal rather than circular).
#    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
#    C2 = np.sqrt(alpha**2 + beta**2)
    
    # Intensity (HSI model).
    I = pixel.mean()
    # Value (HSV "hexcone" model).
    V = M
    # Lightness (HSL "hexcone" model).
    L = .5 * (M+m)
    # Luma (Rec. 601 NTSC).
    Yp601 = .299*pixel[0] + .587*pixel[1] + .114*pixel[2]
    # Luma (Rec. 709).
    Yp709 = .2126*pixel[0] + .7156*pixel[1] + .0722*pixel[2]
    
    # HSV saturation.
#    S_HSV = saturation_HSV(C, V)
    # HSL saturation.
#    S_HSL = saturation_HSL(C, L)
    # HSI saturation.
#    S_HSI = saturation_HSI(C, m, I)
    
    return {
#        'M' : M,
#        'm' : m,
#        'C' : C,
#        'H' : H,
#        'alpha' : alpha,
#        'beta' : beta,
#        'H2' : H2,
#        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
#        'S HSV' : S_HSV,
#        'S HSL' : S_HSL,
#        'S HSI' : S_HSI,
        }

# ----------------------------------------------------------------------

from_RGB_vect = np.vectorize(from_RGB_pixel)

# ======================================================================
# Convert an image from RGB (without vectorization).
# ======================================================================

def from_RGB_wo_vect(img):
    
    # Maximum.
    M = img.max(2)
    # Minimum.
    m = img.min(2)
    # Chroma.
#    C = M - m
    
    # Intensity (HSI model).
    I = img.mean(axis=2)
    # Value (HSV "hexcone" model).
    V = M
    # Lightness (HSL "hexcone" model).
    L = .5 * (M+m)
    # Luma (Rec. 601 NTSC).
    Yp601 = .299*img[:, :, 0] + .587*img[:, :, 1] + .114*img[:, :, 2]
    # Luma (Rec. 709).
    Yp709 = .2126*img[:, :, 0] + .7156*img[:, :, 1] + .0722*img[:, :, 2]
    
#    ly, lx = img.shape[0:2]
#    H = np.empty_like(M, dtype=float)
#    S_HSV = np.empty_like(M, dtype=float)
#    S_HSL = np.empty_like(M, dtype=float)
#    S_HSI = np.empty_like(M, dtype=float)
#    for y in range(ly):
#        for x in range(lx):
            # Hue.
#            H[y, x] = hue(img[y, x, :], C[y, x], M[y, x])
            # HSV saturation.
#            S_HSV[y, x] = saturation_HSV(C[y, x], V[y, x])
            # HSL saturation.
#            S_HSL[y, x] = saturation_HSL(C[y, x], L[y, x])
            # HSI saturation.
#            S_HSI[y, x] = saturation_HSI(C[y, x], m[y, x], I[y, x])
    
    # Alpha.
#    alpha = img[:, :, 0] - .5*(img[:, :, 1] + img[:, :, 2])
    # Beta.
#    beta = half_rt_3 * (img[:, :, 1] - img[:, :, 2])
    # Hue 2 (hexagonal rather than circular).
#    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
#    C2 = np.sqrt(alpha**2 + beta**2)
    
    return {
#        'M' : M,
#        'm' : m,
#        'C' : C,
#        'H' : H,
#        'alpha' : alpha,
#        'beta' : beta,
#        'H2' : H2,
#        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
#        'S HSV' : S_HSV,
#        'S HSL' : S_HSL,
#        'S HSI' : S_HSI,
        }

# ======================================================================
# Convert an image from RGB (with vectorization).
# ======================================================================

def from_RGB_w_vect(img):
    
    # Maximum.
    M = img.max(axis=2)
    # Minimum.
    m = img.min(axis=2)
    # Chroma.
#    C = M - m
    
    # Intensity (HSI model).
    I = img.mean(axis=2)
    # Value (HSV "hexcone" model).
    V = M
    # Lightness (HSL "hexcone" model).
    L = .5 * (M+m)
    # Luma (Rec. 601 NTSC).
    Yp601 = .299*img[:, :, 0] + .587*img[:, :, 1] + .114*img[:, :, 2]
    # Luma (Rec. 709).
    Yp709 = .2126*img[:, :, 0] + .7156*img[:, :, 1] + .0722*img[:, :, 2]
    
    # Hue.
#    H = vect_hue(img, C, M)
    # HSV saturation.
#    S_HSV = vect_saturation_HSV(C, V)
    # HSL saturation.
#    S_HSL = vect_saturation_HSL(C, L)
    # HSI saturation.
#    S_HSI = vect_saturation_HSI(C, m, I)
    
    # Alpha.
#    alpha = img[:, :, 0] - .5*(img[:, :, 1] + img[:, :, 2])
    # Beta.
#    beta = half_rt_3 * (img[:, :, 1] - img[:, :, 2])
    # Hue 2 (hexagonal rather than circular).
#    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
#    C2 = np.sqrt(alpha**2 + beta**2)
    
    return {
#        'M' : M,
#        'm' : m,
#        'C' : C,
#        'H' : H,
#        'alpha' : alpha,
#        'beta' : beta,
#        'H2' : H2,
#        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
#        'S HSV' : S_HSV,
#        'S HSL' : S_HSL,
#        'S HSI' : S_HSI,
        }

# ----------------------------------------------------------------------

def from_RGB_w_vect_2(img):
    
    # Maximum.
    M = img.max(axis=2)
    # Minimum.
    m = img.min(axis=2)
    # Chroma.
#    C = M - m
    # Hue.
#    H = vect_hue(img, C, M)
    
    # Alpha.
#    alpha = img[:, :, 0] - .5*(img[:, :, 1] + img[:, :, 2])
    # Beta.
#    beta = half_rt_3 * (img[:, :, 1] - img[:, :, 2])
    # Hue 2 (hexagonal rather than circular).
#    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
#    C2 = np.sqrt(alpha**2 + beta**2)
    
    # Intensity (HSI model).
    I = img.mean(axis=2)
    # Value (HSV "hexcone" model).
    V = M
    # Lightness (HSL "hexcone" model).
    L = .5 * (M+m)
    # Luma (Rec. 601 NTSC).
    Yp601 = .299*img[:, :, 0] + .587*img[:, :, 1] + .114*img[:, :, 2]
    # Luma (Rec. 709).
    Yp709 = .2126*img[:, :, 0] + .7156*img[:, :, 1] + .0722*img[:, :, 2]
    
    # HSV saturation.
#    S_HSV = vect_saturation_HSV(C, V)
    # HSL saturation.
#    S_HSL = vect_saturation_HSL(C, L)
    # HSI saturation.
#    S_HSI = vect_saturation_HSI(C, m, I)
    
    return {
#        'M' : M,
#        'm' : m,
#        'C' : C,
#        'H' : H,
#        'alpha' : alpha,
#        'beta' : beta,
#        'H2' : H2,
#        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
#        'S HSV' : S_HSV,
#        'S HSL' : S_HSL,
#        'S HSI' : S_HSI,
        }

# ======================================================================
# Hue.
# ======================================================================

def hue(pixel, C, M):
    if (C == 0.):
        return chroma_zero
    elif (M == pixel[0]):
        return (pixel[1]-pixel[2])/C % 6 * hue_scale
    elif (M == pixel[1]):
        return ((pixel[2]-pixel[0])/C + 2.) * hue_scale
    else:
        return ((pixel[0]-pixel[1])/C + 4.) * hue_scale

# ----------------------------------------------------------------------

vect_hue = np.vectorize(hue)

# ======================================================================
# Saturation (HSV).
# ======================================================================

def saturation_HSV(C, V):
    if (C == 0.):
        return 0.
    else:
        if (V == 0):
            print(
                'Warning:\nValue is zero but chroma is nonzero in '
                + 'saturation_HSV.')
        return C / V * scale

# ----------------------------------------------------------------------

vect_saturation_HSV = np.vectorize(saturation_HSV)

# ======================================================================
# Saturation (HSL).
# ======================================================================

def saturation_HSL(C, L):
    if (C == 0.):
        return 0.
    else:
        if (L == 0):
            print(
                'Warning:\nLuminosity is zero but chroma is nonzero in '
                + 'saturation_HSL.')
        return C / (1.-abs(2*L/scale-1))

# ----------------------------------------------------------------------

vect_saturation_HSL = np.vectorize(saturation_HSL)

# ======================================================================
# Saturation (HSI).
# ======================================================================

def saturation_HSI(C, m, I):
    if (C == 0.):
        return 0.
    else:
        if (I == 0):
            print(
                'Warning:\nIntensity is zero but chroma is nonzero in '
                + 'saturation_HSI.')
        return (1. - m/I) * scale

# ----------------------------------------------------------------------

vect_saturation_HSI = np.vectorize(saturation_HSI)

# ======================================================================
