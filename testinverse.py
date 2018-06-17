#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from FNFTpy import *

options = get_nsev_inverse_options(0,0,0,0,2)
print(options.discretization)

def nsev_inverse_xi_wrapper(clib_nsev_inverse_xi_func, D, T1, T2, M, DIS):
    clib_nsev_inverse_xi_func.restype = ctypes_int
    NSEV_D = ctypes_uint(D)
    NSEV_T = np.zeros(2, dtype=numpy_double)
    NSEV_T[0] = T1
    NSEV_T[1] = T2
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


def nsev_inverse_wrapper(clib_nsev_inverse_func, clib_nsev_inverse_xi_func, M, contspec, Xi1, Xi2, K, bound_states,
                         normconst_or_residues, D, T1, T2, kappa,
                         DIS=1, CST=0, CIM=0, MAXITER=100, OSF=8):
    clib_nsev_inverse_func.restype = ctypes_int
    NSEV_M = ctypes_uint(M)
    NSEV_contspec = np.zeros(M, dtype=numpy_complex)
    NSEV_XI = np.zeros(2, dtype=numpy_double)
    NSEV_K = ctypes_uint(K)
    NSEV_boundstates = np.zeros(K,dtype=numpy_complex)
    NSEV_discspec = np.zeros(K, dtype=numpy_complex)
    NSEV_D = ctypes_uint(D)
    NSEV_T = np.zeros(2, dtype=numpy_double)
    NSEV_T[0]=T1
    NSEV_T[1]=T2
    NSEV_kappa = ctypes_int(kappa)
    NSEV_q = np.zeros(NSEV_D.value, dtype=numpy_complex)

    rv, tmpXI = nsev_inverse_xi_wrapper(clib_nsev_inverse_xi_func, D, T1, T2, M, DIS)
    print(rv)



tvec = np.linspace(-14,14,200)
#rv, XI = nsev_inverse_xi_wrapper(fnft_clib.fnft_nsev_inverse_XI, 200, -14,14 , 20, 0)

M  = 11
contspec = np.zeros(M, dtype=np.complex128)
K = 0
T1 = np.min(tvec)
T2 = np.max(tvec)
kappa=1
D = 0

nsev_inverse_wrapper(fnft_clib.fnft_nsev_inverse_XI, fnft_clib.fnft_nsev_inverse,
                     M, contspec, 0, 0, K, None, None, D, T1, T2, kappa)