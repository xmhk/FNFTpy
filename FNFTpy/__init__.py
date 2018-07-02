# import numpy as np
# import ctypes
from .auxiliary import get_lib_path

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper
from .fnft_nsep_wrapper import nsep_wrapper
from .fnft_nsev_wrapper import nsev_wrapper
from .typesdef import *

# get python ctypes object of FNFT
libpath = get_lib_path()  # edit in auxilary.py
fnft_clib = ctypes.CDLL(libpath)


def kdvv(u, tvec, m=128, xi1=-2, xi2=2, dis=15):
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
                [optional, standard=15]
                0 = 2SPLIT1A
                1 = 2SPLIT1B
                2 = 2SPLIT2A
                3 = 2SPLIT2B
                4 = 2SPLIT3A
                5 = 2SPLIT3B
                6 = 2SPLIT4A
                7 = 2SPLIT4B
                8 = 2SPLIT5A
                9 = 2SPLIT5B
                10 = 2SPLIT6A
                11 = 2SPLIT6B
                12 = 2SPLIT7A
                13 = 2SPLIT7B
                14 = 2SPLIT8A
                15 = 2SPLIT8B
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from FNFT
        contspec : continuous spectrum        
    """
    d = len(u)
    k = 0  # not yet implemented
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_kdvv_options(dis)
    return kdvv_wrapper(fnft_clib.fnft_kdvv, d, u, t1, t2, m, xi1, xi2,
                        k, options)


def nsep(q, t1, t2, kappa=1, loc=2, filt=2, bb=None,
         maxev=20, dis=1, nf=1):
    """
    calculates the Nonlinear Fourier Transform for the periodic Nonlinear Schroedinger equation.
    Parameters:
    ----------
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
        return_value : return value from FNFT
        k : number of points in the main spectrum
        main : main spectrum
        m: number of points in the auxillary spectrum
    aux: auxilary spectrum
    """
    if bb is None:  # set standard value for bb
        bb = [-200, 200, -200, 200]
    d = len(q)
    options = get_nsep_options(loc, filt, bb, maxev, dis, nf)
    return nsep_wrapper(fnft_clib.fnft_nsep, d, q, t1, t2,
                        kappa, options)


def nsev(q, tvec, xi1=-2, xi2=2, m=128, k=128, kappa=1, bsf=2,
         bsl=2, niter=10, dst=0, cst=0, nf=1, dis=3):
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
        return_value : return value from FNFT
        bound_states_num : number of bound states found
        bound_states : array of bound states found 
        d_norm : discrete spectrum - norming constants
        d_res : discrete spectrum - residues
        c_ref : continuous spectrum - reflection coefficient
        c_a : continuous spectrum - scattering coefficient a
        c_b : continuous spectrum - scattering coefficient b
    """
    d = len(q)
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_nsev_options(bsf, bsl, niter, dst, cst, nf, dis)
    return nsev_wrapper(fnft_clib.fnft_nsev, d, q, t1, t2, xi1, xi2,
                        m, k, kappa, options)
