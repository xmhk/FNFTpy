import ctypes
import numpy as np
from .auxilary import *

# data types for interfacing C

ctypes_int32 = ctypes.c_int32  # FNFT_INT, (C int32_t )
ctypes_uint = ctypes.c_size_t  # FNFT_UINT (C size_t)
ctypes_int = ctypes.c_int  # plain c integer, e.g. union elements
ctypes_double = ctypes.c_double  # FNFT_REAL
numpy_complex = np.complex128  # FNFT_COMPLEX for Arrays (C-double)
numpy_double = np.double  # FNFT_REAL for Arrays (C-double)


# option structs for interfacing C

class kdvv_options_struct(ctypes.Structure):
    _fields_ = [
        ("discretization", ctypes_int)]


class nsep_options_struct(ctypes.Structure):
    _fields_ = [
        ("localization", ctypes_int),
        ("filtering", ctypes_int),
        ("bounding_box", ctypes_double * 4),
        ("max_evals", ctypes_uint),
        ("discretization", ctypes_int),
        ("normalization_flag", ctypes_int32)]


class nsev_options_struct(ctypes.Structure):
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int32),
        ("discretization", ctypes_int)]


def get_kdvv_options(DIS):
    """returns an options struct for KDVV
    Parameters:
    ----------
        DIS: discretization
           0 = 2SPLIT1A,
           1 = 2SPLIT1B,
           2 = SPLIT2A,
           3 = 2SPLIT2B,
           4 = 2SPLIT3A,
           5 = 2SPLIT3B,
           6 = 2SPLIT4A,
           7 = 2SPLIT4B,
           8 = 2SPLIT5A,
           9 = 2SPLIT5B,
           10 = 2SPLIT6A,
           11 = 2SPLIT6B,
           12 = 2SPLIT7A,
           13 = 2SPLIT7B,
           14 = 2SPLIT8A,
           15 = 2SPLIT8B
    Returns:
    ----------
        options struct for KDVV C call
    """
    check_value(DIS, 0, 15)  # Discretization
    return kdvv_options_struct(DIS)


def get_nsep_options(LOC, FILT, BB, MAXEV, DIS, NF):
    """creates a options struct for NSEP
    Parameters:
    ----------
        LOC : localization of spectrum
              0=Subsample and Refine,
              1=Gridsearch,
              2=Mixed
        FILT : filtering of spectrum
               0=None,
               1=Manual,
               2=Auto
        BB : bounding box used for manual filtering
        MAXEV : maximum number of evaluations for root refinement
        NF : normalization flag
        DIS : discretization  
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO
    Returns:
    ----------
        options struct  for NSEP C call
    """
    check_value(LOC, 0, 2)  # Bound state filtering
    check_value(FILT, 0, 2)  # Bound state localization        
    check_value(NF, 0, 1)  # Normflag
    check_value(DIS, 0, 4)  # Discretization
    BBtype = ctypes_double * 4
    return nsep_options_struct(LOC, FILT, BBtype(BB[0], BB[1], BB[2], BB[3]),
                               MAXEV, DIS, NF)


def get_nsev_options(BSF, BSL, niter, DS, CS, NF, DIS):
    """creates a options struct for NSEV
    Parameters:
    ----------
        BSF : bound state filtering 
               (0=none, 1=basic, 2=full; default=2)
        BSL : bound state localization 
               0=Fast Eigenvalue, 
               1=Newton, 
               2=Subsample and Refine
        niter : number of iterations for Newton BSL
        DS : type of discrete spectrum 
               0=norming constants, 
               1=residues, 
               2=both
        CS : type of continuous spectrum 
               0=reflection coefficient, 
               1=a and b, 
               2=both
        NF : normalization Flag 0=off, 1=on
        DIS : discretization  
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO
    Returns:
    ----------
        options struct  for NSEV C call
    """
    check_value(BSF, 0, 2)  # Bound state filtering
    check_value(BSL, 0, 2)  # Bound state localization    
    check_value(niter, 0, 32000)  # niter
    check_value(DS, 0, 2)  # Discspec type
    check_value(CS, 0, 2)  # Contspec type
    check_value(NF, 0, 1)  # Normflag
    check_value(DIS, 0, 4)  # Discretization
    return nsev_options_struct(BSF, BSL, niter, DS, CS, NF, DIS)
