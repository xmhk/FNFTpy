import numpy as np
import ctypes
from .auxilary import get_lib_path


# get python ctypes object of libFNFT
libpath = get_lib_path()  # edit in auxilary.py
fnft_clib = ctypes.CDLL(libpath)

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper
from .fnft_nsep_wrapper import nsep_wrapper
from .fnft_nsev_wrapper import nsev_wrapper
from .fnft_nsev_inverse_wrapper import nsev_inverse_xi_wrapper, nsev_inverse_wrapper
from .typesdef import *

def kdvv(u, tvec, M=100, xi1=-2, xi2=2, DIS=15):
    """calculates the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries
    Parameters:
    ----------       
        u : numpy array holding the samples of the field to be analyzed        
        tvec : time vector
        M : number of values for the continuous spectrum to calculate, 
            [optional, standard=100]
        xi1, xi2 : min and max frequency for the continuous spectrum, 
                   [optional, standard=-/+ 2]        
        DIS : determines the discretization, [optional, standard=15]
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        contspec : continuous spectrum        
    """
    clib_kdvv_func = fnft_clib.fnft_kdvv
    D = len(u)
    K = 0 # not yet implemented
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_kdvv_options(DIS)
    return kdvv_wrapper(clib_kdvv_func, D, u, t1, t2, M, xi1, xi2,
                        K, options)    

def nsep(q, t1, t2, kappa=1, LOC=2, FILT=2, BB=[-200, 200, -200,200],
         MAXEV=20, DIS=1, NF=1):
    """
    calculates the Nonlinear Fourier Transform for the periodic Nonlinear Schroedinger Equation
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
        q : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the (D+1) sample
        kappa : +/- 1 for focussing/defocussing nonlinearity 
               [optional, standard = +1]
        LOC : localization of spectrum
             0=Subsample and Refine,
             1=Gridsearch,
             2=Mixed [optional, default=2]
        FILT : filtering of spectrum
               0=None,
               1=Manual,
               2=Auto [optional, default=2]
        BB: bounding box used for manual filtering 
            [optional, default=[-200,200,-200,200]]
        MAXEV : maximum number of evaluations for root refinement
                [optional, default=20]
        NF : normalization Flag 0=off, 1=on [optional, default=1]
        DIS : discretization  
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO [optional, default=2] 
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        K : number of points in the main spectrum 
        main : main spectrum
        M: number of points in the auxilary spectrum
	aux: auxilary spectrum
    """
    clib_nsep_func = fnft_clib.fnft_nsep
    D = len(q)
    options = get_nsep_options(LOC, FILT, BB, MAXEV, DIS, NF)
    return nsep_wrapper(clib_nsep_func, D, q, t1, t2,
                        kappa, options)    

    
def nsev(q, tvec, xi1=-2, xi2=2, M=100, K=100, kappa=1, BSF=2, 
         BSL=2, niter=10, DSUB=0, DS=0, CS=0, NF=1, DIS=3):
    """Calculates the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.
    Parameters:
    ----------
        q : numpy array holding the samples of the field to be analyzed
        tvec: time vector for q samples
        xi1, xi2: min and max frequency for the continuous spectrum. [optional, standard = -2,2]
        M: number of values for the continuous spectrum to calculate [optional, standard = 100]
        K: maximum number of bound states to calculate [optional, standard = 100]
        kappa : +/- 1 for focussing/defocussing nonlinearity [optional, standard = +1]
        BSF : bound state filtering 
              0=none, 
              1=basic, 
              2=full; [optional, default=2]
        BSL : bound state localization 
              0=Fast Eigenvalue, 
              1=Newton, 
              2=Subsample and Refine; [optional, default=0]
        niter : number of iterations for Newton BSL [optional, default=10]
        DSUB : manual number of subsamples for refine method [optional, 0=auto]
        DS : type of discrete spectrum 
             0=norming constants, 
             1=residues, 
             2=both; [optional, defaul=2]
        CS type of continuous spectrum 
            0=reflection coefficient, 
            1=a and b, 
            2=both; [optional, default=0]
        NF normalization Flag 
            0=off 
            1=on; [optional, default=1]
        DIS : discretization  
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO; [optional, default=3]
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
    D = len(q)
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_nsev_options(BSF, BSL, niter, DSUB, DS, CS, NF, DIS)
    return nsev_wrapper(clib_nsev_func, D, q, t1, t2, xi1, xi2,
                        M, K, kappa, options)


def nsev_inverse(contspec, tvec, kappa, DIS=1,
                 CST=0, CIM=0, MAXITER=100, OSF=8):
    clib_nsev_inverse_func = fnft_clib.fnft_nsev_inverse
    clib_nsev_inverse_xi_func = fnft_clib.fnft_nsev_inverse_XI
    M = len(contspec)
    D = len(tvec)
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    K=0
    rv, tmpXI = nsev_inverse_xi_wrapper(clib_nsev_inverse_xi_func, D, T1, T2 , M, DIS)
    if rv!=0:
        raise ValueError("nsev_inverse_xi calculation failes")
    options = get_nsev_inverse_options(DIS, CST, CIM, MAXITER, OSF)
    rdict = nsev_inverse_wrapper(clib_nsev_inverse_func,
                              M, contspec, tmpXI[0], tmpXI[1], K, None, None, D, T1, T2, kappa, options)
    return rdict
