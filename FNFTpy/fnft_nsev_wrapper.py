from .typesdef import *

def nsev_wrapper(clib_nsev_func, D, q, t1, t2, xi1, xi2,
        	 M, K, kappa, options):
    """
    FNFT(NSEv) wraps the python input and returns the result from libFNFT
    Parameters:
    ----------
        clib_nsev_func : handle of the c function imported via ctypes
        D : number of sample points
        q : numpy array holding the samples of the field to be analyzed
        t1, t2 : time positions of the first and the last sample
        xi1, xi2 : min and max frequency for the continuous spectrum
        M : number of values for the continuous spectrum to calculate
        K : maximum number of bound states to calculate
        kappa : +/- 1 for focussing/defocussing nonlinearity
        options : options for nsev as nsev_options_struct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        bound_states_num : number of bound states found
        bound_states : array of bound states found 
        d_norm : discrete spectrum - norming constants
        d_res : discrete spectrum - residues
        c_ref : continuous spectrum - reflection coefficient
        c_a : continuous spectrum - scattering coefficient a
        c_b : continuous spectrum - scattering coefficient b
    """      
    clib_nsev_func.restype = ctypes_int    
    NSEV_D = ctypes_uint(D)
    NSEV_M = ctypes_uint(M)
    NSEV_K = ctypes_uint(K)
    NSEV_T = np.zeros(2, dtype=numpy_double)
    NSEV_T[0] = t1
    NSEV_T[1] = t2   
    NSEV_q = np.zeros(NSEV_D.value,dtype=numpy_complex)
    NSEV_q[:] = q[:] + 0.0j
    NSEV_kappa = ctypes_int(kappa)    
    NSEV_XI = np.zeros(2, dtype=numpy_double)
    NSEV_XI[0] = xi1
    NSEV_XI[1] = xi2    
    NSEV_boundstates = np.zeros(K,dtype=numpy_complex)    
    # discrete spectrum -> reflection coefficient and / or residues
    if options.discspec_type==2:
        NSEV_discspec = np.zeros(2 * K,dtype=numpy_complex)
    else:
        NSEV_discspec = np.zeros(K,dtype=numpy_complex)
    # continuous spectrum -> reflection coefficient and / or a,b    
    if options.contspec_type ==0:
        NSEV_contspec = np.zeros(M,dtype=numpy_complex)        
    elif options.contspec_type==1:
        NSEV_contspec = np.zeros(2 * M,dtype=numpy_complex) 
    else:
        NSEV_contspec = np.zeros(3 * M,dtype=numpy_complex)    
    clib_nsev_func.argtypes= [
        type(NSEV_D),                                # D 
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # q
        np.ctypeslib.ndpointer(dtype = ctypes_double,
                               ndim=1, flags='C'),   # T
        type(NSEV_M),                                # M
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # contspec
        np.ctypeslib.ndpointer(dtype = ctypes_double, 
                               ndim=1, flags='C'),   # xi
        ctypes.POINTER(ctypes_uint),                 # K_ptr
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # boundstates
        np.ctypeslib.ndpointer(dtype = numpy_complex, 
                               ndim=1, flags='C'),   # normconst res
        type(NSEV_kappa),                            # kappa
        ctypes.POINTER( nsev_options_struct)]        # options ptr
        
    rv = clib_nsev_func(
        NSEV_D, 
        NSEV_q, 
        NSEV_T, 
        NSEV_M, 
        NSEV_contspec, 
        NSEV_XI, 
        NSEV_K, 
        NSEV_boundstates, 
        NSEV_discspec, 
        NSEV_kappa, 
        ctypes.byref(options))
    K_new = NSEV_K.value
    rdict = {
        'return_value':rv,
        'bound_states_num':K_new,
        'bound_states':NSEV_boundstates[0:K_new]}
    

    if options.discspec_type==0:
        rdict['d_norm'] = NSEV_discspec[0:K_new]
    elif options.discspec_type==1:
        rdict['d_res'] = NSEV_discspec[0:K_new]   
    elif options.discspec_type==2:
        rdict['d_norm'] = NSEV_discspec[0:K_new]  
        rdict['d_res'] = NSEV_discspec[K_new:2*K_new] 
    else:
        pass
    if options.contspec_type ==0:
        rdict['c_ref'] = NSEV_contspec[0:M]       
    elif options.contspec_type==1:
        rdict['c_a'] = NSEV_contspec[0:M]    
        rdict['c_b'] = NSEV_contspec[M:2*M]    
    elif options.contspec_type==2:
        rdict['c_ref'] = NSEV_contspec[0:M] 
        rdict['c_a'] = NSEV_contspec[M:2*M]    
        rdict['c_b'] = NSEV_contspec[2*M:3*M]           
    else:
        pass
    return rdict

