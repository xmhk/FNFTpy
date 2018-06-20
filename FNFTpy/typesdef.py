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

#
# Korteweg-de-Vries (vanishing)
#

class KdvvOptionsStruct(ctypes.Structure):
    _fields_ = [
        ("discretization", ctypes_int)]


def get_kdvv_options(dis):
    """returns an options struct for KDVV
    Parameters:
    ----------
        DIS: discretization
           0 = 2SPLIT1A
           1 = 2SPLIT1B
           2 = SPLIT2A
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
        options struct for KDVV C call
    """
    check_value(dis, 0, 15)  # Discretization
    return KdvvOptionsStruct(dis)

#
# Nonlinear Schroedinger Equation (periodic)
#


class NsepOptionsStruct(ctypes.Structure):
    _fields_ = [
        ("localization", ctypes_int),
        ("filtering", ctypes_int),
        ("bounding_box", ctypes_double * 4),
        ("max_evals", ctypes_uint),
        ("discretization", ctypes_int),
        ("normalization_flag", ctypes_int32)]


def get_nsep_options(loc, filt, bb, maxev, dis, nf):
    """creates a options struct for NSEP
    Parameters:
    ----------
        loc : localization of spectrum
                0=Subsample and Refine
                1=Gridsearch
                2=Mixed
        filt : filtering of spectrum
                 0=None
                 1=Manual
                 2=Auto
        bb : bounding box used for manual filtering
        maxev : maximum number of evaluations for root refinement
        nf : normalization flag
        dis : discretization
                0=2split2modal
                1=2split2a
                2=2split4a
                3=2split4b
                4=BO
    Returns:
    ----------
        options struct  for NSEP C call
    """
    check_value(loc, 0, 2)  # Bound state filtering
    check_value(filt, 0, 2)  # Bound state localization
    check_value(nf, 0, 1)  # Normflag
    check_value(dis, 0, 4)  # Discretization
    bbtype = ctypes_double * 4
    return NsepOptionsStruct(loc, filt, bbtype(bb[0], bb[1], bb[2], bb[3]),
                               maxev, dis, nf)


#
# Nonlinear Schroedinger Equation (vanishing boundaries)
#


class NsevOptionsStruct(ctypes.Structure):
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),
        ("Dsub", ctypes_uint),
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int32),
        ("discretization", ctypes_int)]


class NsevInverseOptionsStruct(ctypes.Structure):
    _fields_ = [
        ("discretization", ctypes_int),
        ("contspec_type", ctypes_int),
        ("contspec_inversion_method", ctypes_int),
        ("max_iter", ctypes_uint),
        ("oversampling_factor", ctypes_uint)
    ]

def get_nsev_options(bsf, bsl, niter, dsub, dst, cst, nf, dis):
    """creates a options struct for NSEV
    Parameters:
    ----------
        bsf : bound state filtering
                0=none
                1=basic
                2=full
        bsl : bound state localization
               0=Fast Eigenvalue
               1=Newton
               2=Subsample and Refine
        niter : number of iterations for Newton BSL
        dsub : manual number of subsamples
        dst : type of discrete spectrum
               0=norming constants
               1=residues
               2=both
        cst : type of continuous spectrum
               0=reflection coefficient
               1=a and b
               2=both
        nf : normalization Flag
               0=off
               1=on
        dis : discretization
               0=2split2modal
               1=2split2a
               2=2split4a
               3=2split4b
               4=BO
    Returns:
    ----------
        options struct  for NSEV C call
    """
    check_value(bsf, 0, 2)  # Bound state filtering
    check_value(bsl, 0, 2)  # Bound state localization
    check_value(niter, 0, 32000)  # niter
    check_value(dsub, 0, 32000)  # Dsub
    check_value(dst, 0, 2)  # Discspec type
    check_value(cst, 0, 2)  # Contspec type
    check_value(nf, 0, 1)  # Normflag
    check_value(dis, 0, 4)  # Discretization
    return NsevOptionsStruct(bsf, bsl, niter, dsub, dst, cst, nf, dis)



def get_nsev_inverse_options(dis, cst, cim, maxiter, osf):
    """returns an options struct for NSEV Inverse
    Parameters:
        dis : Discretization to use
              0=2split2_MODAL
              1=2split2A
              2=2split4A
              3=2split4B
              4=BO
        cst : type of continuous spectrum
                0=reflection coefficient
                1=b of tau
        csi : type of inverse method for continuous spectrum
                0=default
                1=TF-matrix contains reflection coeff.
                2=TF-matrix contains a,b from iteration
        maxiter : maximum number of iterations (continuous spectrum)
        osf : oversampling factor
            """
    check_value(dis, 0, 4)
    check_value(cst, 0, 1)
    check_value(cim, 0, 2)
    check_value(maxiter, 0, 32000)
    check_value(osf, 1, 32000)
    return NsevInverseOptionsStruct(dis, cst, cim, maxiter, osf)

