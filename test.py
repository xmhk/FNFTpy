import numpy as np
from FNFTpy import *


def kdvvtest():
    xvec = np.linspace(-10, 10, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, xi1=-10, xi2=10, dis=15, m=2048)
    print(res['return_value'])


def nseptest():
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsep(q, 0, 2 * np.pi)
    print(res['return_value'])
    res = nsep(q, 0, 2 * np.pi, maxev=40)
    print(res['return_value'])


def nsevtest():
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsev(q, xvec)
    print(res['return_value'])
    res = nsev(q, xvec, dst=2)
    print(res['return_value'])


def kdvvexample():
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(d, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    xi1 = -2
    xi2 = 2
    m = 8
    xivec = np.linspace(xi1, xi2, m)
    res = kdvv(q, tvec, m, xi1=xi1, xi2=xi2, dis=15)
    print("libFNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d. xi=%.4f   %.6f  %.6fj" % (i, xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


def nsepexample():
    d = 256
    dt = 2 * np.pi / d
    tvec = np.arange(d) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
    print("libFNFT return value: %d" % res['return_value'])
    print("number of samples: %d"%d)
    print('main spectrum')
    for i in range(res['k']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
    print('auxilary spectrum')
    for i in range(res['m']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))


def nsevexample():
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    m = 8
    res = nsev(q, tvec, m=m, xi1=-2, xi2=2, k=d)
    xivec = np.linspace(-2, 2, m)
    print("libFNFT return value: %d" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['c_ref'])):
        print("%d xi = %.4f   %.6f  %.6fj" % (i, xivec[i], np.real(res['c_ref'][i]), np.imag(res['c_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                   np.imag(res['bound_states'][i]),
                                                                   np.real(res['d_norm'][i]),
                                                                   np.imag(res['d_norm'][i])))


# detect some general errors
# nsevtest()
# kdvvtest()
# nseptest()

# mimic the example files
#  nsevexample()
#  kdvvexample()
# nsepexample()

