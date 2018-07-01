from .typesdef import *


def kdvv_wrapper(clib_kdvv_func, D, u, T1, T2, M, Xi1, Xi2,
                 K, options):
    """
    Wraps the python input and returns the result from FNFT's fnft_kdvv.
    Parameters:
    ----------
        clib_kdvv_func : handle of the c function imported via ctypes
        D : number of samples
        u : numpy array holding the samples of the field to be analyzed
        T1, T2  : time positions of the first and the last sample
        M : number of values for the continuous spectrum to calculate
        Xi1, Xi2 : min and max frequency for the continuous spectrum
        K : maximum number of bound states to calculate (no effect yet)
        options : options for nsev as nsev_options_struct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        contspec : continuous spectrum        
    """
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
    # kdvv_boundstates = np.zeros(k, dtype=numpy_complex)
    # discrete spectrum -> will stay empty until implemented
    # kdvv_discspec = np.zeros(k, dtype=numpy_complex)
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
