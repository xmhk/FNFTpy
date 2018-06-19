from .typesdef import *


def nsep_wrapper(clib_nsep_func, d, q, t1, t2, kappa,
                 options):
    """
    wraps the python input and returns the result from libFNFT  fnft_nsep
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
        d : number of sample points
        q : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the (d+1) sample
        kappa   : +/- 1 for focussing/defocussing nonlinearity
        options : options for nsev as nsev_options_struct
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        k : number of points in the main spectrum
        main : main spectrum
        m: number of points in the auxilary spectrum
	aux: auxilary spectrum
    """

    clib_nsep_func.restype = ctypes_int
    nsep_d = ctypes_uint(d)
    nsep_q = np.zeros(nsep_d.value, dtype=numpy_complex)
    nsep_q[:] = q[:] + 0.0j
    nsep_t = np.zeros(2, dtype=numpy_double)
    nsep_t[0] = t1
    nsep_t[1] = t2
    nsep_k = ctypes_uint(4 * nsep_d.value)
    nsep_main_spec = np.zeros(nsep_k.value, dtype=numpy_complex)
    nsep_m = ctypes_uint(2 * nsep_d.value)
    nsep_aux_spec = np.zeros(nsep_m.value, dtype=numpy_complex)
    nsep_sheet_indices = ctypes.POINTER(ctypes.c_int)()  # null_pointer
    nsep_kappa = ctypes_int(kappa)

    clib_nsep_func.argtypes = [
        type(nsep_d),  # d
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        ctypes.POINTER(ctypes_uint),  # k_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # main_spec
        ctypes.POINTER(ctypes_uint),  # m_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # aux_spec
        type(nsep_sheet_indices),  # sheet indices
        type(nsep_kappa),  # kappa
        ctypes.POINTER(nsep_options_struct)]  # options ptr

    rv = clib_nsep_func(
        nsep_d,
        nsep_q,
        nsep_t,
        nsep_k,
        nsep_main_spec,
        nsep_m,
        nsep_aux_spec,
        nsep_sheet_indices,
        nsep_kappa,
        ctypes.byref(options))
    rdict = {
        'return_value': rv,
        'K': nsep_k.value,
        'main': nsep_main_spec[0:nsep_k.value],
        'M': nsep_m.value,
        'aux': nsep_aux_spec[0:nsep_m.value]}
    return rdict
