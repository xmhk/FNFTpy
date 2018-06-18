#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 23:10:41 2018

@author: ch
"""
import numpy as np
from FNFTpy import *

def kdvvtest():
    print("KDVV test")
    xvec = np.linspace(-10,10,256)
    q = np.sin(2*np.pi/256 * xvec )
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, xi1=-10, xi2 = 10, DIS=15, M=2048)
    #print(res.keys())

def nseptest():
    print("NSEP test")
    xvec = np.linspace(0, 2*np.pi, 256)
    q = np.sin(2*np.pi/256 * xvec )
    res  = nsep(q, 0, 2*np.pi)
    print(res['return_value'])
    res  = nsep(q, 0, 2*np.pi, MAXEV=40)
    print(res['return_value'])
    
def nsevtest():
    print("NSEV test")
    xvec = np.linspace(0, 2*np.pi, 256)
    q = np.sin(2*np.pi/256 * xvec )
    res  = nsev(q, xvec,DSUB=3, BSL=2)
    print(res['return_value'])
    res  = nsev(q,xvec, DS=2)
    print(res['return_value'])
    
def kdvvexample():
    D = 256
    tvec = np.linspace(-1,1,D)
    q= np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    x1 = -2
    x2 = 2
    M = 8
    res = kdvv(q, tvec, M, xi1=x1, xi2=x2, DIS=15)
    print("libFNFT return value: %d"%res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d   %.6f  %.6fj"%(i, np.real(res['contspec'][i]),np.imag(res['contspec'][i])))

def nsepexample():
    D= 256
    dt = 2*np.pi/D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2*np.pi, BB=[-2,2,-2,2], FILT=1)
    print("libFNFT return value: %d"%res['return_value'])
    print('main spectrum')
    for i in range(res['K']):
        print("%d   %.6f  %.6fj"%(i, np.real(res['main'][i]),np.imag(res['main'][i])))        
    print('auxilary spectrum')
    for i in range(res['M']):
        print("%d   %.6f  %.6fj"%(i, np.real(res['aux'][i]),np.imag(res['aux'][i])))
def nsevexample():
    D=256        
    tvec = np.linspace(-1,1,D)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0+0.0j
    M = 8 
    res = nsev(q, tvec, M=M, xi1=-2, xi2=2, K=D )
    print("libFNFT return value: %d"%res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['c_ref'])):
        print("%d   %.6f  %.6fj"%(i, np.real(res['c_ref'][i]),np.imag(res['c_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d   %.6f  %.6fj with norming const %.6f  %.6fj"%(i, np.real(res['bound_states'][i]),
                                  np.imag(res['bound_states'][i]),
                                  np.real(res['d_norm'][i]),
                                  np.imag(res['d_norm'][i])))

def nsev_inverse_example():
    M = 2048
    D = 1024
    DIS = 1
    tvec = np.linspace(-2, 2, D)
    alpha = 2.0
    beta = -0.55
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    XI1 = 0
    XI2 = 0
    rv, XI = nsev_inverse_xi_wrapper(fnft_clib.fnft_nsev_inverse_XI, D, T1, T2, M, DIS)
    xiv = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)
    contspec = np.zeros(M, dtype=np.complex128)
    contspec = alpha / (xiv - beta * 1.0j)
    kappa = 1

    tvec = np.linspace(-2, 2, D)

    rd = nsev_inverse(contspec,
                      tvec,
                      kappa, OSF=8)
    q = rd['q']

    for i in range(0, D, 64):
        print("t = %.5f     q=%.5e  + %.5e i" % (tvec[i], np.real(q[i]), np.imag(q[i])))
#nsevexample()
#nsepexample()
#kdvvexample()

nsev_inverse_example()
#nsevtest()
#kdvvtest()
#nseptest()


