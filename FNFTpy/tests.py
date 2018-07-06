from .fnft_kdvv_wrapper import *
from .fnft_nsep_wrapper import *
from .fnft_nsev_wrapper import *


def print_default_options():
    kdvvopts = get_kdvv_options()
    print("\n ----\n kdvv default options:\n %s \n\n"%repr(kdvvopts))

    nsepopts = get_nsep_options()
    print("\n ----\n nsep default options:\n %s \n\n" % repr(nsepopts))

    nsevopts = get_nsev_options()
    print("\n ----\n nsev default options:\n %s \n\n" % repr(nsevopts))


def kdvvexample():
    """Mimics the C example for calling fnft_kdvv."""
    print("\n\nkdvv example")

    # set values
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    Xi1 = -2
    Xi2 = 2
    M = 8
    Xivec = np.linspace(Xi1, Xi2, M)

    # call function
    res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2)

    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("continuous spectrum: ")
    for i in range(len(res['cont'])):
        print("%d : Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i],
              np.real(res['cont'][i]), np.imag(res['cont'][i])))


def nsepexample():
    """Mimics the C example for calling fnft_nsep."""
    print("\n\nnsep example")

    # set values
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)

    # call function
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)

    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("number of samples: %d" % D)
    print('main spectrum')
    for i in range(res['K']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                     np.imag(res['main'][i])))
    print('auxiliary spectrum')
    for i in range(res['M']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                     np.imag(res['aux'][i])))


def nsevexample():
    """Mimics the C example for calling fnft_nsev."""
    print("\n\nnsev example")

    # set values
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    M = 8
    Xi1 = -2
    Xi2 = 2
    Xivec = np.linspace(Xi1, Xi2, M)

    # call function
    res = nsev(q, tvec, M=M, Xi1=Xi1, Xi2=Xi2)

    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")

    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['cont_ref'])):
        print("%d :  Xi = %.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['cont_ref'][i]), np.imag(res['cont_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d : %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                 np.imag(res['bound_states'][i]),
                                                                 np.real(res['disc_norm'][i]),
                                                                 np.imag(res['disc_norm'][i])))



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
    res = nsev(q, xvec, Dsub=32)
    print(res['return_value'])
    print(res['options'])

