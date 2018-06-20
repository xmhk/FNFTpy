from .typesdef import *


def kdvv_wrapper(clib_kdvv_func, d, u, t1, t2, m, xi1, xi2,
                 k, options):
    """
    Wraps the python input and returns the result from libFNFT's fnft_kdvv.
    Parameters:
    ----------
        clib_kdvv_func : handle of the c function imported via ctypes
        d : number of samples
        u : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the last sample
        m : number of values for the continuous spectrum to calculate
        xi1, xi2 : min and max frequency for the continuous spectrum        
        k : maximum number of bound states to calculate
        options : options for nsev as KdvvOptionsStruct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        contspec : continuous spectrum        
    """
    clib_kdvv_func.restype = ctypes_int
    kdvv_d = ctypes_uint(d)
    kdvv_u = np.zeros(kdvv_d.value, dtype=numpy_complex)
    kdvv_u[:] = u[:] + 0.0j
    kdvv_t = np.zeros(2, dtype=numpy_double)
    kdvv_t[0] = t1
    kdvv_t[1] = t2
    kdvv_m = ctypes_uint(m)
    kdvv_contspec = np.zeros(m, dtype=numpy_complex)
    kdvv_xi = np.zeros(2, dtype=numpy_double)
    kdvv_xi[0] = xi1
    kdvv_xi[1] = xi2
    # kdvv_k = ctypes_uint(k)
    # bound states -> will stay empty until implemented
    # kdvv_boundstates = np.zeros(k, dtype=numpy_complex)
    # discrete spectrum -> will stay empty until implemented
    # kdvv_discspec = np.zeros(k, dtype=numpy_complex)
    kdvv_nullptr = ctypes.POINTER(ctypes.c_int)()
    clib_kdvv_func.argtypes = [
        type(kdvv_d),  # d
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # u
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(kdvv_m),  # m
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(kdvv_nullptr),  # k_ptr
        type(kdvv_nullptr),  # boundstates
        type(kdvv_nullptr),  # normconsts res
        ctypes.POINTER(KdvvOptionsStruct)]  # options ptr
    rv = clib_kdvv_func(
        kdvv_d,
        kdvv_u,
        kdvv_t,
        kdvv_m,
        kdvv_contspec,
        kdvv_xi,
        kdvv_nullptr,
        kdvv_nullptr,
        kdvv_nullptr,
        ctypes.byref(options))
    rdict = {'return_value': rv, 'contspec': kdvv_contspec}
    return rdict
