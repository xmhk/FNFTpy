from .typesdef import *
from .options_handling import get_kdvv_options, print_kdvv_options
from .auxiliary import get_lib_path


def kdvv(u, tvec, M=128, Xi1=-2, Xi2=2, dis=None):
    """calculates the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.
    Parameters:
    ----------
        u : numpy array holding the samples of the field to be analyzed
        tvec : time vector
        M : number of samples for the continuous spectrum to calculate,
            [optional, standard=128]
        Xi1, Xi2 : min and max frequency for the continuous spectrum,
                   [optional, standard=-/+ 2]
        dis : determines the discretization
                [optional, standard=15]
                0 = 2SPLIT1A
                1 = 2SPLIT1B
                2 = 2SPLIT2A
                3 = 2SPLIT2B
                4 = 2SPLIT3A
                5 = 2SPLIT3B
                6 = 2SPLIT4A
                7 = 2SPLIT4B
                8 = 2SPLIT5A
                9 = 2SPLIT5B
                10 = 2SPLIT6A
                11 = 2SPLIT6B
                12 = 2SPLIT7A
                13 = 2SPLIT7B
                14 = 2SPLIT8A
                15 = 2SPLIT8B
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        contspec : continuous spectrum
    """

    D = len(u)
    K = 0  # not yet implemented
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_kdvv_options(dis=dis)
    print_kdvv_options(options)
    return kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                        K, options)


def kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                 K, options):
    """
    Wraps the python input and returns the result from FNFT's fnft_kdvv
    Parameters:
    ----------
        D : number of samples
        u : numpy array holding the samples of the field to be analyzed
        T1, T2  : time positions of the first and the last sample
        M : number of values for the continuous spectrum to calculate
        Xi1, Xi2 : min and max frequency for the continuous spectrum
        K : maximum number of bound states to calculate (no effect yet)
        options : options for kdvv as KdvvOptionsStruct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        contspec : continuous spectrum        
    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_kdvv_func = fnft_clib.fnft_kdvv
    clib_kdvv_func.restype = ctypes_int
    kdvv_D = ctypes_uint(D)
    kdvv_u = np.zeros(kdvv_D.value, dtype=numpy_complex)
    kdvv_u[:] = u[:] + 0.0j
    kdvv_T = np.zeros(2, dtype=numpy_double)
    kdvv_T[0] = T1
    kdvv_T[1] = T2
    kdvv_M = ctypes_uint(M)
    kdvv_contspec = np.zeros(M, dtype=numpy_complex)
    kdvv_Xi = np.zeros(2, dtype=numpy_double)
    kdvv_Xi[0] = Xi1
    kdvv_Xi[1] = Xi2
    # kdvv_k = ctypes_uint(k)
    # bound states -> will stay empty until implemented
    # kdvv_boundstates = np.zeros(k,dtype=numpy_complex)
    # discrete spectrum -> will stay empty until implemented
    # kdvv_discspec = np.zeros(k,dtype=numpy_complex)
    kdvv_nullptr = ctypes.POINTER(ctypes.c_int)()
    clib_kdvv_func.argtypes = [
        type(kdvv_D),  # D
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # u
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(kdvv_M),  # M
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # Xi
        type(kdvv_nullptr),  # K_ptr
        type(kdvv_nullptr),  # boundstates
        type(kdvv_nullptr),  # normconsts res
        ctypes.POINTER(KdvvOptionsStruct)]  # options ptr
    rv = clib_kdvv_func(
        kdvv_D,
        kdvv_u,
        kdvv_T,
        kdvv_M,
        kdvv_contspec,
        kdvv_Xi,
        kdvv_nullptr,
        kdvv_nullptr,
        kdvv_nullptr,
        ctypes.byref(options))
    rdict = {'return_value': rv, 'contspec': kdvv_contspec}
    return rdict
