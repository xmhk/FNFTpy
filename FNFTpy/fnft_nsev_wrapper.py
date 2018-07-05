from .typesdef import *
from .auxiliary import *
from .options_handling import print_nsev_options, get_nsev_options


def nsev(q, tvec, Xi1=-2, Xi2=2, M=128, K=128, kappa=1, bsf=None,
         bsl=None, niter=None, dst=None, cst=None, nf=None, dis=None):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.

    This function is intended to be 'clutter-free', which means it automatically calculates some variables
    needed to call the C-library.
    Options can be set by passing optional arguments (see below).
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'nsev_wrapper' can be used (see documentation there).


    Arguments:

        q : numpy array holding the samples of the field to be analyzed

        tvec: time vector for q samples

    Optional Arguments:

        Xi1, Xi2 : min and max frequency for the continuous spectrum. default = -2,2

        M : number of values for the continuous spectrum to calculate default = 128

        K : maximum number of bound states to calculatem default = 128

        kappa : +/- 1 for focussing/defocussing nonlinearity, default = 1


        bsf : bound state filtering, default =2

            0=none
            1=basic
            2=full

        bsl : bound state localization, default = 0

            0=Fast Eigenvalue
            1=Newton
            2=Subsample and Refine

        niter : number of iterations for Newton bound state localization, default = 10

        dst : type of discrete spectrum, default = 2

            0=norming constants
            1=residues
            2=both

        cst : type of continuous spectrum, default = 0

            0=reflection coefficient
            1=a and b
            2=both

        nf : normalization flag, default = 1

            0=off
            1=on

        dis : discretization, default = 3

            0=2spliT2modal
            1=2spliT2a
            2=2split4a
            3=2split4b
            4=BO

    Returns:

        rdict : dictionary holding the fields (depending on options)

            return_value : return value from FNFT

            bound_states_num : number of bound states found

            bound_states : array of bound states found

            d_norm : discrete spectrum - norming constants

            d_res : discrete spectrum - residues

            c_ref : continuous spectrum - reflection coefficient

            c_a : continuous spectrum - scattering coefficient a

            c_b : continuous spectrum - scattering coefficient b

    """
    D = len(q)
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_nsev_options(bsf=bsf, bsl=bsl, niter=niter, dst=dst, cst=cst, nf=nf, dis=dis)
    return nsev_wrapper(D, q, T1, T2, Xi1, Xi2,
                        M, K, kappa, options)


def nsev_wrapper(D, q, T1, T2, Xi1, Xi2,
                 M, K, kappa, options):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.

    This function's interface mimics the behavior of the function 'fnft_nsev' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'nsev' can be used (see documentation there).

    Arguments:


        D : number of sample points

        q : numpy array holding the samples of the field to be analyzed

        T1, T2 : time positions of the first and the last sample

        Xi1, Xi2 : min and max frequency for the continuous spectrum

        M : number of values for the continuous spectrum to calculate

        K : maximum number of bound states to calculate

        kappa : +/- 1 for focussing/defocussing nonlinearity

        options : options for nsev as NsevOptionsStruct


    Returns:

        rdict : dictionary holding the fields (depending on options)

            return_value : return value from FNFT

            bound_states_num : number of bound states found

            bound_states : array of bound states found

            d_norm : discrete spectrum - norming constants

            d_res : discrete spectrum - residues

            c_ref : continuous spectrum - reflection coefficient

            c_a : continuous spectrum - scattering coefficient a

            c_b : continuous spectrum - scattering coefficient b

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_nsev_func = fnft_clib.fnft_nsev
    clib_nsev_func.restype = ctypes_int
    nsev_D = ctypes_uint(D)
    nsev_M = ctypes_uint(M)
    nsev_K = ctypes_uint(K)
    nsev_T = np.zeros(2, dtype=numpy_double)
    nsev_T[0] = T1
    nsev_T[1] = T2
    nsev_q = np.zeros(nsev_D.value, dtype=numpy_complex)
    nsev_q[:] = q[:] + 0.0j
    nsev_kappa = ctypes_int(kappa)
    nsev_Xi = np.zeros(2, dtype=numpy_double)
    nsev_Xi[0] = Xi1
    nsev_Xi[1] = Xi2
    nsev_boundstates = np.zeros(K, dtype=numpy_complex)
    # discrete spectrum -> reflection coefficient and / or residues
    if options.discspec_type == 2:
        nsev_discspec = np.zeros(2 * K, dtype=numpy_complex)
    else:
        nsev_discspec = np.zeros(K, dtype=numpy_complex)
    # continuous spectrum -> reflection coefficient and / or a,b    
    if options.contspec_type == 0:
        nsev_contspec = np.zeros(M, dtype=numpy_complex)
    elif options.contspec_type == 1:
        nsev_contspec = np.zeros(2 * M, dtype=numpy_complex)
    else:
        nsev_contspec = np.zeros(3 * M, dtype=numpy_complex)
    clib_nsev_func.argtypes = [
        type(nsev_D),  # D
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(nsev_M),  # M
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # contspec
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        ctypes.POINTER(ctypes_uint),  # K_ptr
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # boundstates
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # normconst res
        type(nsev_kappa),  # kappa
        ctypes.POINTER(NsevOptionsStruct)]  # options ptr

    rv = clib_nsev_func(
        nsev_D,
        nsev_q,
        nsev_T,
        nsev_M,
        nsev_contspec,
        nsev_Xi,
        nsev_K,
        nsev_boundstates,
        nsev_discspec,
        nsev_kappa,
        ctypes.byref(options))
    K_new = nsev_K.value
    rdict = {
        'return_value': rv,
        'bound_states_num': K_new,
        'bound_states': nsev_boundstates[0:K_new]}

    if options.discspec_type == 0:
        rdict['d_norm'] = nsev_discspec[0:K_new]
    elif options.discspec_type == 1:
        rdict['d_res'] = nsev_discspec[0:K_new]
    elif options.discspec_type == 2:
        rdict['d_norm'] = nsev_discspec[0:K_new]
        rdict['d_res'] = nsev_discspec[K_new:2 * K_new]
    else:
        pass
    if options.contspec_type == 0:
        rdict['c_ref'] = nsev_contspec[0:M]
    elif options.contspec_type == 1:
        rdict['c_a'] = nsev_contspec[0:M]
        rdict['c_b'] = nsev_contspec[M:2 * M]
    elif options.contspec_type == 2:
        rdict['c_ref'] = nsev_contspec[0:M]
        rdict['c_a'] = nsev_contspec[M:2 * M]
        rdict['c_b'] = nsev_contspec[2 * M:3 * M]
    else:
        pass
    return rdict
