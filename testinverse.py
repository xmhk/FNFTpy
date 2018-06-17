#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from FNFTpy import *

options = get_nsev_inverse_options(0,0,0,0,2)
print(options.discretization)

def inverse_xi_wrapper(clib_nsev_inverse_xi_func, tvec, M, DIS):
    clib_nsev_inverse_xi_func.restype = ctypes_int
    NSEV_D = ctypes_uint(len(tvec))
    NSEV_T = np.zeros(2, dtype=numpy_double)
    NSEV_T[0] = np.min(tvec)
    NSEV_T[1] = np.max(tvec)
    NSEV_M = ctypes_uint(M)
    NSEV_XI = np.zeros(2, dtype=numpy_double)
    NSEV_DIS = ctypes_int32(DIS)
    clib_nsev_inverse_xi_func.argtypes = [
        type(NSEV_D),  # D
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # T
        type(NSEV_M),  # M
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(NSEV_DIS)]
    rv =clib_nsev_inverse_xi_func(
            NSEV_D,
            NSEV_T,
            NSEV_M,
            NSEV_XI,
            DIS)
    return rv, NSEV_XI


tvec = np.linspace(-14,14,200)
rv, XI = inverse_xi_wrapper(fnft_clib.fnft_nsev_inverse_XI, tvec, 20, 0)