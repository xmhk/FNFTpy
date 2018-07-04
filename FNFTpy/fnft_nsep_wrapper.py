from .typesdef import *


def fnft_nsep_default_opts_wrapper(clib_func):
    """
        Call the default options for nsep directly from the library
        Returns:
            NsepOptionsStruct: holding default options
        """
    clib_func.restype = NsepOptionsStruct
    clib_func.argtpes=[]
    return clib_func()

def nsep_wrapper(clib_nsep_func, D, q, T1, T2, kappa,
                 options):
    """
    Wraps the python input and returns the result from FNFT's fnft_nsep.
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
        D : number of sample points
        q : numpy array holding the samples of the field to be analyzed
        T1, T2  : time positions of the first and the (D+1) sample
        kappa   : +/- 1 for focussing/defocussing nonlinearity
        options : options for nsep as NsepOptionsStruct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        K : number of points in the main spectrum
        main : main spectrum
        M: number of points in the auxiliary spectrum
        aux: auxiliary spectrum"""

    clib_nsep_func.restype = ctypes_int  
    nsep_D = ctypes_uint(D)
    nsep_q = np.zeros(nsep_D.value, dtype=numpy_complex)
    nsep_q[:] = q[:] + 0.0j
    nsep_T = np.zeros(2, dtype=numpy_double)
    nsep_T[0] = T1
    nsep_T[1] = T2
    nsep_K = ctypes_uint(4 * nsep_D.value)
    nsep_main_spec = np.zeros(nsep_K.value, dtype=numpy_complex)
    nsep_M = ctypes_uint(2 * nsep_D.value)
    nsep_aux_spec = np.zeros(nsep_M.value, dtype=numpy_complex)
    nsep_sheet_indices = ctypes.POINTER(ctypes.c_int)()  # null_pointer
    nsep_kappa = ctypes_int(kappa)

    clib_nsep_func.argtypes = [
        type(nsep_D),                                # D
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),   # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),   # t
        ctypes.POINTER(ctypes_uint),                 # K_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),   # main_spec
        ctypes.POINTER(ctypes_uint),                 # M_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),   # aux_spec    
        type(nsep_sheet_indices),                    # sheet indices
        type(nsep_kappa),                            # kappa
        ctypes.POINTER(NsepOptionsStruct)]         # options ptr
        
    rv = clib_nsep_func(
        nsep_D,
        nsep_q,
        nsep_T,
        nsep_K,
        nsep_main_spec,
        nsep_M,
        nsep_aux_spec,
        nsep_sheet_indices,
        nsep_kappa,
        ctypes.byref(options))
    rdict = { 
        'return_value': rv,
        'K': nsep_K.value,
        'main': nsep_main_spec[0:nsep_K.value],
        'M': nsep_M.value,
        'aux': nsep_aux_spec[0:nsep_M.value]}
    return rdict
