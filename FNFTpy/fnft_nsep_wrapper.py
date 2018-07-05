from .typesdef import *
from .auxiliary import get_lib_path
# libpath = get_lib_path()  # edit in auxiliary.py
# fnft_clib = ctypes.CDLL(libpath)
from .options_handling import print_nsep_options, get_nsep_options


def nsep(q, T1, T2, kappa=1, loc=None, filt=None, bb=None,
         maxev=None, dis=None, nf=None):
    """
    calculates the Nonlinear Fourier Transform for the periodic Nonlinear Schroedinger equation.
    Parameters:
    ----------
        q : numpy array holding the samples of the field to be analyzed
        T1, T2  : time positions of the first and the (d+1) sample
        kappa : +/- 1 for focussing/defocussing nonlinearity
               [optional, standard = +1]
        loc : localization of spectrum
                [optional, default=2]
                0=Subsample and Refine
                1=Gridsearch
                2=Mixed
        filt : filtering of spectrum
                 [optional, default=2]
                 0=None
                 1=Manual
                 2=Auto
        bb: bounding box used for manual filtering
            [optional, default=None (bb is set to [-200,200,-200,200])]
        maxev : maximum number of evaluations for root refinement
                [optional, default=20]
        nf : normalization Flag 0=off, 1=on [optional, default=1]
        dis : discretization
                [optional, default=2]
                0=2spliT2modal
                1=2spliT2a
                2=2split4a
                3=2split4b
                4=BO
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        K : number of points in the main spectrum
        main : main spectrum
        m: number of points in the auxiliary spectrum
    aux: auxiliary spectrum
    """
    D = len(q)
    options = get_nsep_options(loc=loc, filt=filt, bb=bb, maxev=maxev, dis=dis, nf=nf)
    print_nsep_options(options)
    return nsep_wrapper(D, q, T1, T2,
                        kappa, options)


def nsep_wrapper(D, q, T1, T2, kappa,
                 options):
    """
    Wraps the python input and returns the result from FNFT's fnft_nsep.
    Parameters:
    ----------
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
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_nsep_func = fnft_clib.fnft_nsep
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
        type(nsep_D),  # D
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        ctypes.POINTER(ctypes_uint),  # K_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # main_spec
        ctypes.POINTER(ctypes_uint),  # M_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # aux_spec
        type(nsep_sheet_indices),  # sheet indices
        type(nsep_kappa),  # kappa
        ctypes.POINTER(NsepOptionsStruct)]  # options ptr

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
