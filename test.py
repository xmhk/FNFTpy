import numpy as np
from FNFTpy import *


def kdvvtest():
    print("KDVV test")
    xvec = np.linspace(-10, 10, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, Xi1=-10, Xi2=10, dis=15, M=2048)
    print(res['return_value'])


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
    res = nsev(q, xvec)
    print(res['return_value'])
    res = nsev(q, xvec, dst=2)
    print(res['return_value'])


def kdvvexample():
    print("KDVV example")
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(d, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    Xi1 = -2
    Xi2 = 2
    m = 8
    Xivec = np.linspace(Xi1, Xi2, m)
    res = kdvv(q, tvec, m, Xi1=Xi1, Xi2=Xi2, dis=15)
    print("FNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d. Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


def nsepexample():
    print("NSEP example")
    d = 256
    dt = 2 * np.pi / d
    tvec = np.arange(d) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
    print("FNFT return value: %d" % res['return_value'])
    print("number of samples: %d"%d)
    print('main spectrum')
    for i in range(res['K']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
    print('auXiliary spectrum')
    for i in range(res['M']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))


def nsevexample():
    print("NSEV example")
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    m = 8
    res = nsev(q, tvec, M=m, Xi1=-2, Xi2=2, K=d)
    Xivec = np.linspace(-2, 2, m)
    print("FNFT return value: %d" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['c_ref'])):
        print("%d Xi = %.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['c_ref'][i]), np.imag(res['c_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                   np.imag(res['bound_states'][i]),
                                                                   np.real(res['d_norm'][i]),
                                                                   np.imag(res['d_norm'][i])))


# detect some general errors
nsevtest()
kdvvtest()
nseptest()

# mimic the example files
nsevexample()
kdvvexample()
nsepexample()

