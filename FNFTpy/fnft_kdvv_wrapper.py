from .typesdef import *

def kdvv_wrapper(clib_kdvv_func, D, u, t1, t2, M,  xi1, xi2,  
                 K, options):
    """
    wraps the python input and returns the result from libFNFT  fnft_kdvv
    Parameters:
    ----------
        clib_kdvv_func : handle of the c function imported via ctypes
        D : number of samples	     
        u : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the last sample
        M : number of values for the continuous spectrum to calculate
        xi1, xi2 : min and max frequency for the continuous spectrum        
        K : maximum number of bound states to calculate
        options : options for nsev as nsev_options_struct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        contspec : continuous spectrum        
    """      
    clib_kdvv_func.restype = ctypes_int
    KDVV_D = ctypes_uint(D)
    KDVV_u = np.zeros(KDVV_D.value,dtype=numpy_complex)
    KDVV_u[:] = u[:] + 0.0j
    KDVV_T = np.zeros(2, dtype=numpy_double)
    KDVV_T[0] = t1
    KDVV_T[1] = t2
    KDVV_M = ctypes_uint(M)    
    KDVV_contspec = np.zeros(M,dtype=numpy_complex)
    KDVV_XI = np.zeros(2, dtype=numpy_double)
    KDVV_XI[0] = xi1
    KDVV_XI[1] = xi2
    KDVV_K = ctypes_uint(K)
    # bound states -> will stay empty until implemented
    KDVV_boundstates = np.zeros(K,dtype=numpy_complex)
    # discrete spectrum -> will stay empty until implemented
    KDVV_discspec = np.zeros(K,dtype=numpy_complex)
    KDVV_nullptr = ctypes.POINTER(ctypes.c_int)()    
    clib_kdvv_func.argtypes= [
        type(KDVV_D),                                # D
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # u
        np.ctypeslib.ndpointer(dtype = ctypes_double, 
                               ndim=1, flags='C'),   # T
        type(KDVV_M),                                # M
        np.ctypeslib.ndpointer(dtype = numpy_complex,
                               ndim=1, flags='C'),   # contspec
        np.ctypeslib.ndpointer(dtype = ctypes_double,
                               ndim=1, flags='C'),   # xi
        type(KDVV_nullptr),                          # K_ptr
        type(KDVV_nullptr),                          # boundstates
        type(KDVV_nullptr),                          # normconsts res
        ctypes.POINTER( kdvv_options_struct)]        # options ptr
    rv = clib_kdvv_func(
            KDVV_D,
            KDVV_u,
            KDVV_T, 
            KDVV_M, 
            KDVV_contspec, 
            KDVV_XI,
            KDVV_nullptr,
            KDVV_nullptr,
            KDVV_nullptr,
            ctypes.byref(options))
    rdict = {'return_value':rv , 'contspec': KDVV_contspec}    
    return rdict
