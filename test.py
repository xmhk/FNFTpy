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
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    Xi1 = -2
    Xi2 = 2
    M = 8
    Xivec = np.linspace(Xi1, Xi2, M)
    res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2, dis=15)
    print("FNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d. Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


def nsepexample():
    print("NSEP example")
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
    print("FNFT return value: %d" % res['return_value'])
    print("number of samples: %d"%D)
    print('main spectrum')
    for i in range(res['K']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
    print('auxiliary spectrum')
    for i in range(res['M']):
        print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))


def nsevexample():
    print("NSEV example")
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    M = 8
    res = nsev(q, tvec, M=M, Xi1=-2, Xi2=2, K=D)
    Xivec = np.linspace(-2, 2, M)
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


def kdvvexample2():
    print("KDVV example")
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    Xi1 = -2
    Xi2 = 2
    M = 8
    Xivec = np.linspace(Xi1, Xi2, M)
    #res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2, dis=15)
    D = len(q)
    K = 0  # not yet implemented
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    #options = get_kdvv_options(dis)
    options = get_kdvv_default_wrapper()
    res =  kdvv_wrapper(fnft_clib.fnft_kdvv, D, q, T1, T2, M, Xi1, Xi2,
                        K, options)



    print("FNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d. Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))


t1 = get_kdvv_default_wrapper()
print("dis", t1.discretization)
print("--")


t2 = get_nsep_default_wrapper()
print("loc", t2.localization)
print("filt", t2.filtering)
print("bb", t2.bounding_box[0], t2.bounding_box[1], t2.bounding_box[2], t2.bounding_box[3])
print("max_evals", t2.max_evals)
print("discretization", t2.discretization)
print("normalization flag", t2.normalization_flag)



print("---")
t3 = get_nsev_default_wrapper()
print("bound state loclization", t3.bound_state_localization)
print("niter", t3.niter)
print("discspec_type", t3.discspec_type)
print("contspec_type", t3.contspec_type)
print("discretization", t3.discretization)
print("normalization flag", t3.normalization_flag)

print("--")
kdvvexample2()
kdvvexample()



#("bound_state_filtering", ctypes_int),
#        ("bound_state_localization", ctypes_int),
#        ("niter", ctypes_uint),
#        ("discspec_type", ctypes_int),
#        ("contspec_type", ctypes_int),
#        ("normalization_flag", ctypes_int32),
#        ("discretization", ctypes_int)]


# detect some general errors
#nsevtest()
#kdvvtest()
#nseptest()

# mimic the example files

#nsevexample()
#kdvvexample()
#nsepexample()

