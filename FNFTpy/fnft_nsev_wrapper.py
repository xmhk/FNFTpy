from .typesdef import *


def nsev_wrapper(clib_nsev_func, d, q, t1, t2, xi1, xi2,
                 m, k, kappa, options):
    """
    Wraps the python input and returns the result from libFNFT's fnft_nsev.
    Parameters:
    ----------
        clib_nsev_func : handle of the c function imported via ctypes
        d : number of sample points
        q : numpy array holding the samples of the field to be analyzed
        t1, t2 : time positions of the first and the last sample
        xi1, xi2 : min and max frequency for the continuous spectrum
        m : number of values for the continuous spectrum to calculate
        k : maximum number of bound states to calculate
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
    nsev_d = ctypes_uint(d)
    nsev_m = ctypes_uint(m)
    nsev_k = ctypes_uint(k)
    nsev_t = np.zeros(2, dtype=numpy_double)
    nsev_t[0] = t1
    nsev_t[1] = t2
    nsev_q = np.zeros(nsev_d.value, dtype=numpy_complex)
    nsev_q[:] = q[:] + 0.0j
    nsev_kappa = ctypes_int(kappa)
    nsev_xi = np.zeros(2, dtype=numpy_double)
    nsev_xi[0] = xi1
    nsev_xi[1] = xi2
    nsev_boundstates = np.zeros(k, dtype=numpy_complex)
    # discrete spectrum -> reflection coefficient and / or residues
    if options.discspec_type == 2:
        nsev_discspec = np.zeros(2 * k, dtype=numpy_complex)
    else:
        nsev_discspec = np.zeros(k, dtype=numpy_complex)
    # continuous spectrum -> reflection coefficient and / or a,b    
    if options.contspec_type == 0:
        nsev_contspec = np.zeros(m, dtype=numpy_complex)
    elif options.contspec_type == 1:
        nsev_contspec = np.zeros(2 * m, dtype=numpy_complex)
    else:
        nsev_contspec = np.zeros(3 * m, dtype=numpy_complex)
    clib_nsev_func.argtypes = [
        type(nsev_d),  # d
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(nsev_m),  # m
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        ctypes.POINTER(ctypes_uint),  # k_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # boundstates
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # normconst res
        type(nsev_kappa),  # kappa
        ctypes.POINTER(NsevOptionsStruct)]  # options ptr

    rv = clib_nsev_func(
        nsev_d,
        nsev_q,
        nsev_t,
        nsev_m,
        nsev_contspec,
        nsev_xi,
        nsev_k,
        nsev_boundstates,
        nsev_discspec,
        nsev_kappa,
        ctypes.byref(options))
    k_new = nsev_k.value
    rdict = {
        'return_value': rv,
        'bound_states_num': k_new,
        'bound_states': nsev_boundstates[0:k_new]}

    if options.discspec_type == 0:
        rdict['d_norm'] = nsev_discspec[0:k_new]
    elif options.discspec_type == 1:
        rdict['d_res'] = nsev_discspec[0:k_new]
    elif options.discspec_type == 2:
        rdict['d_norm'] = nsev_discspec[0:k_new]
        rdict['d_res'] = nsev_discspec[k_new:2 * k_new]
    else:
        pass
    if options.contspec_type == 0:
        rdict['c_ref'] = nsev_contspec[0:m]
    elif options.contspec_type == 1:
        rdict['c_a'] = nsev_contspec[0:m]
        rdict['c_b'] = nsev_contspec[m:2 * m]
    elif options.contspec_type == 2:
        rdict['c_ref'] = nsev_contspec[0:m]
        rdict['c_a'] = nsev_contspec[m:2 * m]
        rdict['c_b'] = nsev_contspec[2 * m:3 * m]
    else:
        pass
    return rdict
