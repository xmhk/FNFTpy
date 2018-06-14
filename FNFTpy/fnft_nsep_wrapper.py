from .typesdef import *

def nsep_wrapper(clib_nsep_func, D, q, t1, t2, kappa,
                 options):
    """
    FNFT(NSEP) wraps the python input and returns the result from libFNFT
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
        D : number of sample points
        q : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the (D+1) sample
        kappa   : +/- 1 for focussing/defocussing nonlinearity
        options : options for nsev as nsev_options_struct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        K : number of points in the main spectrum 
        main : main spectrum
        M: number of points in the auxilary spectrum
	aux: auxilary spectrum
    """      

             
    clib_nsep_func.restype = ctypes_int  
    if options==None:
        options=get_nsep_options()
    NSEP_D = ctypes_uint(D)
    NSEP_q = np.zeros(NSEP_D.value,dtype=numpy_complex)
    NSEP_q[:] = q[:] + 0.0j
    NSEP_T = np.zeros(2, dtype=numpy_double)
    NSEP_T[0] = t1
    NSEP_T[1] = t2
    NSEP_K = ctypes_uint(4 * NSEP_D.value)
    NSEP_main_spec = np.zeros(NSEP_K.value,dtype=numpy_complex)
    NSEP_M = ctypes_uint(2 * NSEP_D.value)
    NSEP_aux_spec = np.zeros(NSEP_M.value,dtype=numpy_complex)
    NSEP_sheet_indices = ctypes.POINTER(ctypes.c_int)() # null_pointer
    NSEP_kappa = ctypes_int(kappa)

    clib_nsep_func.argtypes=  [
        type(NSEP_D),                                # D 
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # q
        np.ctypeslib.ndpointer(dtype = ctypes_double, 
                               ndim=1, flags='C'),   # T
        ctypes.POINTER(ctypes_uint),                 # K_ptr
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # main_spec
        ctypes.POINTER(ctypes_uint),                 # M_ptr
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # aux_spec    
        type(NSEP_sheet_indices),                    # sheet indices
        type(NSEP_kappa),                            # kappa
        ctypes.POINTER(nsep_options_struct)]         # options ptr
        
    rv = clib_nsep_func(
        NSEP_D, 
        NSEP_q, 
        NSEP_T,
        NSEP_K,
        NSEP_main_spec,
        NSEP_M, 
        NSEP_aux_spec, 
        NSEP_sheet_indices,  
        NSEP_kappa,
        ctypes.byref(options))
    rdict = { 
        'return_value':rv,
        'K':NSEP_K.value,
        'main':NSEP_main_spec[0:NSEP_K.value],
        'M':NSEP_M.value,
        'aux':NSEP_aux_spec[0:NSEP_M.value]}
    return rdict