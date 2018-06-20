# import numpy as np
# import ctypes
from .auxilary import get_lib_path

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper
from .fnft_nsep_wrapper import nsep_wrapper
from .fnft_nsev_wrapper import nsev_wrapper
from .fnft_nsev_inverse_wrapper import nsev_inverse_xi_wrapper, nsev_inverse_wrapper
from .typesdef import *

# get python ctypes object of libFNFT
libpath = get_lib_path()  # edit in auxilary.py
fnft_clib = ctypes.CDLL(libpath)


def kdvv(u, tvec, m=128, xi1=-2, xi2=2, dis=17):
    """calculates the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.
    Parameters:
    ----------       
        u : numpy array holding the samples of the field to be analyzed        
        tvec : time vector
        m : number of samples for the continuous spectrum to calculate,
            [optional, standard=128]
        xi1, xi2 : min and max frequency for the continuous spectrum, 
                   [optional, standard=-/+ 2]        
        dis : determines the discretization
                [optional, standard=17]
                0 = 2SPLIT1A
                1 = 2SPLIT1B
                2 = 2SPLIT2A
                3 = 2SPLIT2B
                4 = 2SPLIT2S
                5 = 2SPLIT3A
                6 = 2SPLIT3B
                7 = 2SPLIT3S
                8 = 2SPLIT4A
                9 = 2SPLIT4B
                10 = 2SPLIT5A
                11 = 2SPLIT5B
                12 = 2SPLIT6A
                13 = 2SPLIT6B
                14 = 2SPLIT7A
                15 = 2SPLIT7B
                16 = 2SPLIT8A
                17 = 2SPLIT8B
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        contspec : continuous spectrum        
    """
    clib_kdvv_func = fnft_clib.fnft_kdvv
    d = len(u)
    k = 0  # not yet implemented
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_kdvv_options(dis)
    return kdvv_wrapper(clib_kdvv_func, d, u, t1, t2, m, xi1, xi2,
                        k, options)


def nsep(q, t1, t2, kappa=1, loc=2, filt=2, bb=None,
         maxev=20, dis=1, nf=1):
    """
    calculates the Nonlinear Fourier Transform for the periodic Nonlinear Schroedinger equation.
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
        q : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the (d+1) sample
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
                0=2split2modal
                1=2split2a
                2=2split4a
                3=2split4b
                4=BO
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        k : number of points in the main spectrum
        main : main spectrum
        m: number of points in the auxilary spectrum
    aux: auxilary spectrum
    """
    clib_nsep_func = fnft_clib.fnft_nsep
    if bb is None:
        bb = [-200, 200, -200, 200]
    d = len(q)
    options = get_nsep_options(loc, filt, bb, maxev, dis, nf)
    return nsep_wrapper(clib_nsep_func, d, q, t1, t2,
                        kappa, options)


def nsev(q, tvec, xi1=-2, xi2=2, m=128, k=128, kappa=1, bsf=2,
         bsl=2, niter=10, dsub=0, dst=0, cst=0, nf=1, dis=3):
    """Calculates the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.
    Parameters:
    ----------
        q : numpy array holding the samples of the field to be analyzed
        tvec: time vector for q samples
        xi1, xi2 : min and max frequency for the continuous spectrum. [optional, standard = -2,2]
        m : number of values for the continuous spectrum to calculate [optional, standard = 128]
        k : maximum number of bound states to calculate [optional, standard = 128]
        kappa : +/- 1 for focussing/defocussing nonlinearity [optional, standard = +1]
        bsf : bound state filtering
                [optional, default=2]
                0=none
                1=basic
                2=full
        bsl : bound state localization
                [optional, default=0]
                0=Fast Eigenvalue
                1=Newton
                2=Subsample and Refine
        niter : number of iterations for Newton bsl [optional, default=10]
        dsub : manual number of subsamples for refine method [optional, 0=auto]
        dst : type of discrete spectrum
               [optional, defaul=2]
               0=norming constants
               1=residues
               2=both
        cst : type of continuous spectrum
               [optional, default=0]
               0=reflection coefficient
               1=a and b
               2=both
        nf : normalization Flag
               [optional, default=1]
               0=off
               1=on
        dis : discretization
                [optional, default=3]
                0=2split2modal
                1=2split2a
                2=2split4a
                3=2split4b
                4=BO
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
    clib_nsev_func = fnft_clib.fnft_nsev
    d = len(q)
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_nsev_options(bsf, bsl, niter, dsub, dst, cst, nf, dis)
    return nsev_wrapper(clib_nsev_func, d, q, t1, t2, xi1, xi2,
                        m, k, kappa, options)


def nsev_inverse(contspec, tvec, kappa, dis=1,
                 cst=0, cim=0, maxiter=100, osf=8):
    """
    Calculates the Inverse Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.

    ! currently not what you might expect. time and frequency vector can not be chosen independently now ...
    Parameters:
    ----------
        m : number of sample points for continuous spectrum
        tvec : output time vector
        kappa : +1/-1 for focussing / defocussing NSE
        dis : discretization
                [optional, default=1]
                0=2split2_MODAL
                1=2split2A
                2=2split4A
                3=2split4B
                4=BO
        cst : type of continuous spectrum
                [optional, default=0]
                0=reflection coefficient
                1=b of tau
        csi : type of inverse method for continuous spectrum
                [optional, default=0]
                0=default
                1=TF-matrix contains reflection coeff.
                2=TF-matrix contains a,b from iteration
        maxiter : maximum number of iterations (continuous spectrum)
                   [optional, default=100]
        osf : oversampling factor
                [optional, default=8]

        options : options for nsev_inverse as NsevInverseOptionsStruct
    """
    clib_nsev_inverse_func = fnft_clib.fnft_nsev_inverse
    clib_nsev_inverse_xi_func = fnft_clib.fnft_nsev_inverse_XI
    m = len(contspec)
    d = len(tvec)
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    k = 0
    rv, tmpxi = nsev_inverse_xi_wrapper(clib_nsev_inverse_xi_func, d, t1, t2, m, dis)
    if rv != 0:
        raise ValueError("nsev_inverse_xi calculation failes")
    options = get_nsev_inverse_options(dis, cst, cim, maxiter, osf)
    rdict = nsev_inverse_wrapper(clib_nsev_inverse_func,
                                 m, contspec, tmpxi[0], tmpxi[1], k, None, None, d, t1, t2, kappa, options)
    return rdict
