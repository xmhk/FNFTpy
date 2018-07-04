# import numpy as np
# import ctypes
from .auxiliary import get_lib_path

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper
from .fnft_nsep_wrapper import nsep_wrapper
from .fnft_nsev_wrapper import nsev_wrapper
from .typesdef import *

# get python ctypes object of FNFT
libpath = get_lib_path()  # edit in auxiliary.py
fnft_clib = ctypes.CDLL(libpath)




def get_kdvv_default_wrapper():
    fnft_kdvv_default_opts_fun = fnft_clib.fnft_kdvv_default_opts
    fnft_kdvv_default_opts_fun.restype = KdvvOptionsStruct
    #fnft_kdvv_default_opts_fun.restype = ctypes.Structure
    fnft_kdvv_default_opts_fun.argtpes=[]

    test1 = fnft_kdvv_default_opts_fun()
    return test1

def get_nsep_default_wrapper():
    fnft_nsep_default_opts_fun = fnft_clib.fnft_nsep_default_opts
    fnft_nsep_default_opts_fun.restype = NsepOptionsStruct
    #fnft_nsep_default_opts_fun.restype = ctypes.Structure
    fnft_nsep_default_opts_fun.argtpes=[]

    test1 = fnft_nsep_default_opts_fun()
    return test1

def get_nsev_default_wrapper():
    fnft_nsev_default_opts_fun = fnft_clib.fnft_nsev_default_opts
    fnft_nsev_default_opts_fun.restype = NsevOptionsStruct
    #fnft_nsev_default_opts_fun.restype = ctypes.Structure
    fnft_nsev_default_opts_fun.argtpes=[]
    test1 = fnft_nsev_default_opts_fun()
    return test1




def kdvv(u, tvec, M=128, Xi1=-2, Xi2=2, dis=15):
    """calculates the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.
    Parameters:
    ----------       
        u : numpy array holding the samples of the field to be analyzed        
        tvec : time vector
        M : number of samples for the continuous spectrum to calculate,
            [optional, standard=128]
        Xi1, Xi2 : min and max frequency for the continuous spectrum, 
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
    D = len(u)
    K = 0  # not yet implemented
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_kdvv_options(dis)
    return kdvv_wrapper(fnft_clib.fnft_kdvv, D, u, T1, T2, M, Xi1, Xi2,
                        K, options)


def nsep(q, T1, T2, kappa=1, loc=2, filt=2, bb=None,
         maxev=20, dis=1, nf=1):
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
    if bb is None:  # set standard value for bb
        bb = [-200, 200, -200, 200]
    D = len(q)
    options = get_nsep_options(loc, filt, bb, maxev, dis, nf)
    return nsep_wrapper(fnft_clib.fnft_nsep, D, q, T1, T2,
                        kappa, options)


def nsev(q, tvec, Xi1=-2, Xi2=2, M=128, K=128, kappa=1, bsf=2,
         bsl=2, niter=10, dst=0, cst=0, nf=1, dis=3):
    """Calculates the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.
    Parameters:
    ----------
        q : numpy array holding the samples of the field to be analyzed
        tvec: time vector for q samples
        Xi1, Xi2 : min and max frequency for the continuous spectrum. [optional, standard = -2,2]
        M : number of values for the continuous spectrum to calculate [optional, standard = 128]
        K : maximum number of bound states to calculate [optional, standard = 128]
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
                0=2spliT2modal
                1=2spliT2a
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
    D = len(q)
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_nsev_options(bsf, bsl, niter, dst, cst, nf, dis)
    return nsev_wrapper(fnft_clib.fnft_nsev, D, q, T1, T2, Xi1, Xi2,
                        M, K, kappa, options)
