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
# 256. / 6. = 128. / 3. : Hue range of [0, 256).
hue_scale = 1. / 6.

# Constant for calculation of beta.
half_rt_3 = np.sqrt(3.) / 2.

# ======================================================================
# Convert a single pixel from RGB.
# ======================================================================

def pixel_from_RGB(pixel):
    # pixel[0] is red, pixel[1] is green, and pixel[2] is blue.
    
    # Maximum.
    M = pixel.max()
    # Minimum.
    m = img.min()
    # Chroma.
    C = M - m
    # Hue.
    H = hue(pixel, C, M)
    
    # Alpha.
    alpha = pixel[0] - .5*(pixel[1] + pixel[2])
    # Beta.
    beta = half_rt_3 * (pixel[1] - pixel[2])
    # Hue 2 (hexagonal rather than circular).
    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
    C2 = np.sqrt(alpha**2 + beta**2)
    
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
    S_HSV = saturation_HSV(C, V)
    # HSL saturation.
    S_HSL = saturation_HSL(C, L)
    # HSI saturation.
    S_HSI = saturation_HSI(C, m, I)
    
    return {
        'M' : M,
        'm' : m,
        'C' : C,
        'H' : H,
        'alpha' : alpha,
        'beta' : beta,
        'H2' : H2,
        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
        'S HSV' : S_HSV,
        'S HSL' : S_HSL,
        'S HSI' : S_HSI,
        }

# ======================================================================
# Convert an image from RGB.
# ======================================================================

def img_from_RGB(img):
    # img[:, :, 0] is red, img[:, :, 1] is green, and img[:, :, 2] is
    # blue.
    
    # Maximum.
    M = img.max(axis=2)
    # Minimum.
    m = img.min(axis=2)
    # Chroma.
    C = M - m
    
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
    
    ly, lx = img.shape[0:2]
    H = np.empty_like(M)
    S_HSV = np.empty_like(M)
    S_HSL = np.empty_like(M)
    S_HSI = np.empty_like(M)
    for y in range(ly):
        for x in range(lx):
            # Hue.
            H[y, x] = hue(img[y, x, :], C[y, x], M[y, x])
            # HSV saturation.
            S_HSV[y, x] = saturation_HSV(C[y, x], V[y, x])
            # HSL saturation.
            S_HSL[y, x] = saturation_HSL(C[y, x], L[y, x])
            # HSI saturation.
            S_HSI[y, x] = saturation_HSI(C[y, x], m[y, x], I[y, x])
    
    # Alpha.
    alpha = img[:, :, 0] - .5*(img[:, :, 1] + img[:, :, 2])
    # Beta.
    beta = half_rt_3 * (img[:, :, 1] - img[:, :, 2])
    # Hue 2 (hexagonal rather than circular).
    H2 = np.arctan(beta, alpha)
    # Chroma 2 (hexagonal rather than circular).
    C2 = np.sqrt(alpha**2 + beta**2)
    
    return {
        'M' : M,
        'm' : m,
        'C' : C,
        'H' : H,
        'alpha' : alpha,
        'beta' : beta,
        'H2' : H2,
        'C2' : C2,
        'I' : I,
        'V' : V,
        'L' : L,
        'Yp601' : Yp601,
        'Yp709' : Yp709,
        'S HSV' : S_HSV,
        'S HSL' : S_HSL,
        'S HSI' : S_HSI,
        }

# ======================================================================
# RGB to C.
# ======================================================================

def RGB_C(img=None, ret_M=False, ret_m=False, M=None, m=None):
    if (img is not None):
        if (M is None):
            M = img.max(2)
        if (m is None):
            m = img.min(2)
    ret = [M-m,]
    if ret_M:
        ret += [M,]
    if ret_m:
        ret += [m,]
    if (len(ret) == 1):
        return ret[0]
    else:
        return ret

# ======================================================================
# RGB to H.
# ======================================================================

def RGB_H(img, ret_C=False, ret_M=False, ret_m=False):
    if ret_m:
        C, M, m = RGB_C(img, ret_M=True, ret_m=True)
    else:
        C, M = RGB_C(img, ret_M=True)
    H = np.empty_like(C)
    ly, lx = H.shape
    for y in range(ly):
        for x in range(lx):
            H[y, x] = hue(img[y, x, :], C[y, x], M[y, x])
    ret = [H,]
    if ret_C:
        ret += [C,]
    if ret_M:
        ret += [M,]
    if ret_m:
        ret += [m,]
    if (len(ret) == 1):
        return ret[0]
    else:
        return ret

# ----------------------------------------------------------------------

def hue(pixel, C, M):
    if (C == 0.):
        return chroma_zero
    elif (M == pixel[0]):
        return (pixel[1]-pixel[2])/C % 6 * hue_scale
    elif (M == pixel[1]):
        return ((pixel[2]-pixel[0])/C + 2.) * hue_scale
    else  # elif (M == pixel[2]).
        return ((pixel[0]-pixel[1])/C + 4.) * hue_scale

vect_hue = np.vectorize(hue)

# ======================================================================
# RGB to alpha.
# ======================================================================

def RGB_alpha(img):
    return img[:, :, 0] - .5*(img[:, :, 1] + img[:, :, 2])

# ======================================================================
# RGB to beta.
# ======================================================================

def RGB_beta(img):
    return half_rt_3 * (img[:, :, 1] - img[:, :, 2])

# ======================================================================
# RGB to H2.
# ======================================================================

def RGB_H2(img=None, ret_alpha=False, ret_beta=False, alpha=None, beta=None)
    if (img is not None):
        if (alpha is None):
            alpha = RGB_alpha(img)
        if (beta is None):
            beta = RGB_beta(img)
    ret = [np.arctan(beta, alpha),]
    if ret_alpha:
        ret += [alpha,]
    if ret_beta:
        ret += [beta,]
    if (len(ret) == 1):
        return ret[0]
    else:
        return ret

# ======================================================================
# RGB to C2.
# ======================================================================

def RGB_C2(img=None, ret_alpha=False, ret_beta=False, alpha=None, beta=None)
    if (img is not None):
        if (alpha is None):
            alpha = RGB_alpha(img)
        if (beta is None):
            beta = RGB_beta(img)
    ret = [np.sqrt(alpha**2 + beta**2),]
    if ret_alpha:
        ret += [alpha,]
    if ret_beta:
        ret += [beta,]
    if (len(ret) == 1):
        return ret[0]
    else:
        return ret

# ======================================================================
# RGB to S (HSV).
# ======================================================================

def saturation_HSV(C, V):
    if (C == 0.):
        return 0.
    else:
        return C / V

vect_saturation_HSV = np.vectorize(saturation_HSV)

    # HSV saturation.
    S_HSV = saturation_HSV(C, V)

# ======================================================================
# RGB to S (HSL).
# ======================================================================

def saturation_HSL(C, L):
    if (C == 0.):
        return 0.
    else:
        return C / (1.-abs(2*L-1))

vect_saturation_HSL = np.vectorize(saturation_HSL)

    # HSL saturation.
    S_HSL = saturation_HSL(C, L)

# ======================================================================
# RGB to S (HSI).
# ======================================================================

def saturation_HSI(C, m, I):
    if (C == 0.):
        return 0.
    else:
        return 1. - m/I

vect_saturation_HSI = np.vectorize(saturation_HSI)

    # HSI saturation.
    S_HSI = saturation_HSI(C, m, I)

# ======================================================================
# RGB to V.
# ======================================================================

def RGB_V(img):
    return img.max(2)

# ======================================================================
# RGB to L.
# ======================================================================

def RGB_L(img=None, ret_M=False, ret_m=False, M=None, m=None):
    if (img is not None):
        if (M is None):
            M = img.max(2)
        if (m is None):
            m = img.min(2)
    ret = [.5*(M+m),]
    if ret_M:
        ret += [M,]
    if ret_m:
        ret += [m,]
    if (len(ret) == 1):
        return ret[0]
    else:
        return ret

# ======================================================================
# RGB to I.
# ======================================================================

def RGB_I(img):
    return img.mean(2)

# ======================================================================
# Luma (Rec. 601 NTSC).
# RGB to Y'_{601}.
# ======================================================================

def RGB_Yp601(img):
    return .299*img[:, :, 0] + .587*img[:, :, 1] + .114*img[:, :, 2]
    

# ======================================================================
# Luma (Rec. 709).
# RGB to Y'_{709}.
# ======================================================================

def RGB_Yp709(img):
    return .2126*img[:, :, 0] + .7156*img[:, :, 1] + .0722*img[:, :, 2]

# ======================================================================
# RGB to HSV.
# ======================================================================



# ======================================================================
# RGB to HSL.
# ======================================================================



# ======================================================================
# RGB to HSI.
# ======================================================================



