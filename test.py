#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from FNFTpy import *


def kdvvtest():
    print("KDVV test")
    xvec = np.linspace(-10, 10, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, xi1=-10, xi2=10, dis=15, m=2048)
    # print(res.keys())


def nseptest():
    print("NSEP test")
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsep(q, 0, 2 * np.pi)
    print(res['return_value'])
    res = nsep(q, 0, 2 * np.pi, maxev=40)
    print(res['return_value'])


def nsevtest():
    print("NSEV test")
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsev(q, xvec, dsub=3, bsl=2)
    print(res['return_value'])
    res = nsev(q, xvec, ds=2)
    print(res['return_value'])


def nsev_inverse_test():
    print("NSEV inverse")
    M = 2048
    D = 1024
    dis = 1
    tvec = np.linspace(-2, 2, D)
    alpha = 2.0
    beta = -0.55
    kappa = 1
    rv, XI = nsev_inverse_xi_wrapper(fnft_clib.fnft_nsev_inverse_XI, D, np.min(tvec),
                                     np.max(tvec), M, dis)
    xiv = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)
    contspec = np.zeros(M, dtype=np.complex128)
    contspec = alpha / (xiv - beta * 1.0j)
    rd = nsev_inverse(contspec, tvec, kappa, osf=8)
    print("return value ", rd['return_value'])


def kdvvexample():
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    x1 = -2
    x2 = 2
    m = 8
    res = kdvv(q, tvec, m, xi1=x1, xi2=x2, dis=15)
    print("libFNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d   %.6f  %.6fj" % (i, np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


def nsepexample():
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
    print("libFNFT return value: %d" % res['return_value'])
    print('main spectrum')
    for i in range(res['K']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
    print('auxilary spectrum')
    for i in range(res['M']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))


def nsevexample():
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    m = 8
    res = nsev(q, tvec, m=m, xi1=-2, xi2=2, k=d)
    print("libFNFT return value: %d" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['c_ref'])):
        print("%d   %.6f  %.6fj" % (i, np.real(res['c_ref'][i]), np.imag(res['c_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d   %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                   np.imag(res['bound_states'][i]),
                                                                   np.real(res['d_norm'][i]),
                                                                   np.imag(res['d_norm'][i])))


def nsev_inverse_example():
    M = 2048
    D = 1024
    dis = 1
    tvec = np.linspace(-2, 2, D)
    alpha = 2.0
    beta = -0.55
    kappa = 1
    rv, XI = nsev_inverse_xi_wrapper(fnft_clib.fnft_nsev_inverse_XI, D, np.min(tvec),
                                     np.max(tvec), M, dis)
    xiv = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)
    contspec = np.zeros(M, dtype=np.complex128)
    contspec = alpha / (xiv - beta * 1.0j)
    rd = nsev_inverse(contspec, tvec, kappa, osf=8)
    q = rd['q']
    for i in range(0, D, 64):
        print("t = %.5f     q=%.5e  + %.5e i" % (tvec[i], np.real(q[i]), np.imag(q[i])))


nsevexample()
nsepexample()
kdvvexample()
nsev_inverse_test()
nsev_inverse_example()
nsevtest()
kdvvtest()
nseptest()
