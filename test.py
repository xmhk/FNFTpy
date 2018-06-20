#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 23:10:41 2018

@author: ch
"""
import numpy as np
from FNFTpy import *


def kdvvtest():
    xvec = np.linspace(-10, 10, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, xi1=-10, xi2=10, DIS=15, M=2048)
    print(res['return_value'])


def nseptest():
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsep(q, 0, 2 * np.pi)
    print(res['return_value'])
    res = nsep(q, 0, 2 * np.pi, MAXEV=40)
    print(res['return_value'])


def nsevtest():
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsev(q, xvec)
    print(res['return_value'])
    res = nsev(q, xvec, DS=2)
    print(res['return_value'])


def kdvvexample():
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    x1 = -2
    x2 = 2
    M = 8
    res = kdvv(q, tvec, M, xi1=x1, xi2=x2, DIS=15)
    print("libFNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d   %.6f  %.6fj" % (i, np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


def nsepexample():
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2 * np.pi, BB=[-2, 2, -2, 2], FILT=1)
    print("libFNFT return value: %d" % res['return_value'])
    print('main spectrum')
    for i in range(res['k']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
    print('auxilary spectrum')
    for i in range(res['m']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))


def nsevexample():
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    M = 8
    res = nsev(q, tvec, M=M, xi1=-2, xi2=2, K=D, )
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


nsevexample()
# kdvvexample()
# nsepexample()

nsevtest()
# kdvvtest()
# nseptest()
