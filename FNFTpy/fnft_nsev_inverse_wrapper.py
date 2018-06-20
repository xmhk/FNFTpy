from .typesdef import *


def nsev_inverse_xi_wrapper(clib_nsev_inverse_xi_func, d, t1, t2, m, dis):
    """
        Helper function to calculate the spectral borders from the time window.
        Parameters:
        ----------
            clib_nsev_inverse_xi_func : handle of the c function imported via ctypes
            d : number of sample points for the time window
            t1, t2 : borders of the time window
            m : number of samples for the continuous spectrum
            dis : nse discretization parameter
        Returns:
        ----------
        rv : return value of the C-function
        xi : two-element C double vector containing XI borders (frequency)
        """
    clib_nsev_inverse_xi_func.restype = ctypes_int
    nsev_d = ctypes_uint(d)
    nsev_t = np.zeros(2, dtype=numpy_double)
    nsev_t[0] = t1
    nsev_t[1] = t2
    nsev_m = ctypes_uint(m)
    nsev_xi = np.zeros(2, dtype=numpy_double)
    nsev_dis = ctypes_int32(dis)
    clib_nsev_inverse_xi_func.argtypes = [
        type(nsev_d),  # d
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(nsev_m),  # m
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(nsev_dis)]
    rv = clib_nsev_inverse_xi_func(nsev_d, nsev_t, nsev_m, nsev_xi, dis)
    return rv, nsev_xi


def nsev_inverse_wrapper(clib_nsev_inverse_func,
                         m, contspec, xi1, xi2, k, bound_states,
                         normconst_or_residues, d, t1, t2, kappa,
                         options):
    """
    Wraps the python input and returns the result from libFNFT's fnft_nsev_inverse.
    Parameters:
    ----------
        clib_nsev_inverse_func : handle of the c function imported via ctypes
        m : number of sample points for continuous spectrum
        contspec : numpy array holding the samples of the continuous spectrum
        xi1, xi2  : frequencies defining the frequency range (cont spectrum)
        k : number of bound states (currently not effect)
        bound_states : bound states (currently not effect)
        normconst_or_residues : bound state spectral coefficients (currently not effect)
        d : number of samples for the output field
        t1, t2 : borders of the desired time window
        kappa : +1/-1 for focussing / defocussing NSE
        options : options for nsev_inverse as NsevInverseOptionsStruct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        q : time field resulting from inverse transform
    """
    clib_nsev_inverse_func.restype = ctypes_int
    nsev_m = ctypes_uint(m)
    nsev_contspec = np.zeros(m, dtype=numpy_complex)
    nsev_contspec[:] = contspec[:]
    nsev_xi = np.zeros(2, dtype=numpy_double)
    nsev_xi[0] = xi1
    nsev_xi[1] = xi2
    nsev_k = ctypes_uint(k)
    # nsev_boundstates = np.zeros(k,dtype=numpy_complex)
    # nsev_discspec = np.zeros(k, dtype=numpy_complex)
    nsev_d = ctypes_uint(d)
    nsev_t = np.zeros(2, dtype=numpy_double)
    nsev_t[0] = t1
    nsev_t[1] = t2
    nsev_kappa = ctypes_int(kappa)
    nsev_q = np.zeros(nsev_d.value, dtype=numpy_complex)
    nsev_nullptr = ctypes.POINTER(ctypes.c_int)()
    clib_nsev_inverse_func.argtypes = [
        type(nsev_m),
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(nsev_k),
        type(nsev_nullptr),  # boundstates (tmp)
        # np.ctypeslib.ndpointer(dtype=numpy_complex,
        #                       ndim=1, flags='C'),  # boundstates
        type(nsev_nullptr),  # normconst_res (tmp)
        # np.ctypeslib.ndpointer(dtype=numpy_complex,
        #                       ndim=1, flags='C'),  # normconst res
        type(nsev_d),
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(nsev_kappa),
        ctypes.POINTER(NsevInverseOptionsStruct)  # options ptr
    ]
    rv = clib_nsev_inverse_func(
        nsev_m,
        nsev_contspec,
        nsev_xi,
        nsev_k,
        nsev_nullptr,  # boundstates
        nsev_nullptr,  # normconst
        nsev_d,
        nsev_q,
        nsev_t,
        nsev_kappa,
        ctypes.byref(options)
    )
    rdict = {
        'return_value': rv,
        'q': nsev_q
    }
    return rdict
