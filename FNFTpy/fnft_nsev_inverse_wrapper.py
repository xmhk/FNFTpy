from .typesdef import *


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
    rv =clib_nsev_inverse_xi_func(NSEV_D, NSEV_T, NSEV_M, NSEV_XI, DIS)
    return rv, NSEV_XI



def nsev_inverse_wrapper(clib_nsev_inverse_func,
                         M, contspec, Xi1, Xi2, K, bound_states,
                         normconst_or_residues, D, T1, T2, kappa,
                         options):
    clib_nsev_inverse_func.restype = ctypes_int
    NSEV_M = ctypes_uint(M)
    NSEV_contspec = np.zeros(M, dtype=numpy_complex)
    NSEV_contspec[:] = contspec[:]
    NSEV_XI = np.zeros(2, dtype=numpy_double)
    NSEV_XI[0] = Xi1
    NSEV_XI[1] = Xi2
    NSEV_K = ctypes_uint(K)
    #NSEV_boundstates = np.zeros(K,dtype=numpy_complex)
    #NSEV_discspec = np.zeros(K, dtype=numpy_complex)
    NSEV_D = ctypes_uint(D)
    NSEV_T = np.zeros(2, dtype=numpy_double)
    NSEV_T[0]=T1
    NSEV_T[1]=T2
    NSEV_kappa = ctypes_int(kappa)
    NSEV_q = np.zeros(NSEV_D.value, dtype=numpy_complex)
    NSEV_nullptr = ctypes.POINTER(ctypes.c_int)()
    clib_nsev_inverse_func.argtypes = [
        type(NSEV_M),
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(NSEV_K),
        type(NSEV_nullptr),                          # boundstates (tmp)
        #np.ctypeslib.ndpointer(dtype=numpy_complex,
        #                       ndim=1, flags='C'),  # boundstates
        type(NSEV_nullptr),  # normconst_res (tmp)
        #np.ctypeslib.ndpointer(dtype=numpy_complex,
        #                       ndim=1, flags='C'),  # normconst res
        type(NSEV_D),
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # T
        type(NSEV_kappa),
        ctypes.POINTER( nsev_inverse_options_struct)  # options ptr
        ]
    rv = clib_nsev_inverse_func(
        NSEV_M,
        NSEV_contspec,
        NSEV_XI,
        NSEV_K,
        NSEV_nullptr,   # boundstates
        NSEV_nullptr,  # normconst
        NSEV_D,
        NSEV_q,
        NSEV_T,
        NSEV_kappa,
        ctypes.byref(options)
    )
    rdict = {
        'return_value': rv,
        'q' : NSEV_q
    }
    return rdict

