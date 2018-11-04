"""
This file is part of FNFTpy.
FNFTpy provides wrapper functions to interact with FNFT,
a library for the numerical computation of nonlinear Fourier transforms.

For FNFTpy to work, a copy of FNFT has to be installed.
For general information, source files and installation of FNFT,
visit FNFT's github page: https://github.com/FastNFT

For information about setup and usage of FNFTpy see README.md or documentation.

FNFTpy is free software; you can redistribute it and/or
modify it under the terms of the version 2 of the GNU General
Public License as published by the Free Software Foundation.

FNFTpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Contributors:

Christoph Mahnke, Shrinivas Chimmalgi 2018

"""

from .typesdef import *
from .auxiliary import *
from .options_handling import get_nsev_inverse_options


def nsev_inverse(xivec, tvec, contspec, bound_states, discspec,
                  dis=None, cst=None, csim=None, dst=None, max_iter=None, osf=None, kappa=1):
    """Calculate the  Inverse Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.

    This function is intended to be 'clutter-free', which means it automatically calculates some variables
    needed to call the C-library.
    Options can be set by passing optional arguments (see below).
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'nsev_inverse_wrapper' can be used (see documentation there).


    !!! Attention: time and frequency vector can not be choosen independently (yet).
      use nsev_inverse_xi_wrapper to calculate xivec forom tvec !!!

    Arguments:

    * xivec: frequency vector
    * tvec: time vector
    * contspec: continuous spectrum (of xi).  Pass None if for pure soliton state.
    * bound_states: array holding the bound states. Pass None if no bound states present.
    * discspec: discrete spectrum. Pass None if no bound states present.

    Optional arguments:

    * dis : discretization, default = 4

        * 0 = 2SPLIT2_MODAL
        * 1 = BO
        * 2 = 2SPLIT1A
        * 3 = 2SPLIT1B
        * 4 = 2SPLIT2A
        * 5 = 2SPLIT2B
        * 6 = 2SPLIT2S
        * 7 = 2SPLIT3A
        * 8 = 2SPLIT3B
        * 9 = 2SPLIT3S
        * 10 = 2SPLIT4A
        * 11 = 2SPLIT4B
        * 12 = 2SPLIT5A
        * 13 = 2SPLIT5B
        * 14 = 2SPLIT6A
        * 15 = 2SPLIT6B
        * 16 = 2SPLIT7A
        * 17 = 2SPLIT7B
        * 18 = 2SPLIT8A
        * 19 = 2SPLIT8B

    * cst : type of continuous spectrum, default = 0

        * 0 = Reflection coefficient
        * 1 = b of xi
        * 2 = b of tau

    * csim : inversion method for the continuous part, default = 0

        * 0 = default
        * 1 = Transfermatrix with reflection coefficients
        * 2 = Transfermatrix with a,b from iteration
        * 3 = seed potential

    *  dst : type of discrete spectrum, default = 0

        * 0 = norming constants
        * 1 = residues

    * max_iter : maximum number of iterations for iterative methods, default = 100
    * osf : oversampling factor, default = 8

    """
    M = len(xivec)
    D = len(tvec)
    if bound_states is not None:
        K = len(bound_states)
    else:
        K = 0
    if contspec is None:
        M = 0
    options = get_nsev_inverse_options(dis, cst, csim, dst, max_iter, osf)
    rdict = nsev_inverse_wrapper(M, contspec, xivec[0], xivec[-1], K, bound_states, discspec, D, tvec[0], tvec[-1],
                                 kappa, options)
    return rdict


def nsev_inverse_wrapper(M, contspec, Xi1, Xi2, K, bound_states,
                         normconst_or_residues, D, T1, T2, kappa,
                         options):
    """Calculate the  Inverse Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.

    This function's interface mimics the behavior of the function 'fnft_nsev_inverse' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'nsev_inverse' can be used (see documentation there).

    Arguments:

    * M : number of sample points for continuous spectrum
    * contspec : numpy array holding the samples of the continuous spectrum (can be None if M=0)
    * Xi1, Xi2  : frequencies defining the frequency range of the continuous spectrum.
                    ! Currently, the positions returned by nsev_inverse_xi_wrapper must be used !
    * K : number of bound states
    * bound_states : bound states (can be None if K=0)
    * normconst_or_residues : bound state spectral coefficients (can be None if K=0)
    * D : number of samples for the output field
    * T1, T2 : borders of the desired time window
    * kappa : +1/-1 for focussing / defocussing NSE
    * options : options for nsev_inverse as NsevInverseOptionsStruct

    Returns:

    * rdict : dictionary holding the fields (depending on options)

        * return_value : return value from FNFT
        * q : time field resulting from inverse transform
        * options : options for nsev_inverse as NsevInverseOptionsStruct
    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_nsev_inverse_func = fnft_clib.fnft_nsev_inverse
    clib_nsev_inverse_func.restype = ctypes_int
    nsev_nullptr = ctypes.POINTER(ctypes.c_int)()
    nsev_M = ctypes_uint(M)
    nsev_Xi = np.zeros(2, dtype=numpy_double)
    nsev_Xi[0] = Xi1
    nsev_Xi[1] = Xi2
    nsev_K = ctypes_uint(K)
    if (K > 0 and M!=0):  # at least one bound state present
        nsev_contspec = np.zeros(M, dtype=numpy_complex)
        nsev_contspec[:] = contspec[:]
        nsev_boundstates = np.zeros(K, dtype=numpy_complex)
        nsev_boundstates[:] = bound_states[:]
        nsev_discspec = np.zeros(K, dtype=numpy_complex)
        nsev_discspec[:] = normconst_or_residues[:]
        nsev_bstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                                             ndim=1, flags='C')
        nsev_dstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                                             ndim=1, flags='C')
        nsev_cstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C')  # contspec
    elif (K > 0 and M == 0):  # no continuous spectrum
        nsev_contspec = nsev_nullptr
        nsev_boundstates = np.zeros(K, dtype=numpy_complex)
        nsev_boundstates[:] = bound_states[:]
        nsev_discspec = np.zeros(K, dtype=numpy_complex)
        nsev_discspec[:] = normconst_or_residues[:]
        nsev_bstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                                             ndim=1, flags='C')
        nsev_dstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                                             ndim=1, flags='C')
        nsev_cstype = type(nsev_nullptr)
    else:  # no bound states
        nsev_contspec = np.zeros(M, dtype=numpy_complex)
        nsev_contspec[:] = contspec[:]
        nsev_cstype = np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C')  # contspec
        nsev_boundstates = nsev_nullptr
        nsev_discspec = nsev_nullptr
        nsev_bstype = type(nsev_nullptr)
        nsev_dstype = type(nsev_nullptr)

    nsev_D = ctypes_uint(D)
    nsev_T = np.zeros(2, dtype=numpy_double)
    nsev_T[0] = T1
    nsev_T[1] = T2
    nsev_kappa = ctypes_int(kappa)
    nsev_q = np.zeros(nsev_D.value, dtype=numpy_complex)
    clib_nsev_inverse_func.argtypes = [
        type(nsev_M),
        nsev_cstype,  # contspec type
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # xi
        type(nsev_K),  
        nsev_bstype,  # boundstates type
        nsev_dstype,  # normconstants or residues type
        type(nsev_D),
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # q
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(nsev_kappa),
        ctypes.POINTER(NsevInverseOptionsStruct)  # options ptr
    ]
    rv = clib_nsev_inverse_func(
        nsev_M,
        nsev_contspec,
        nsev_Xi,
        nsev_K,
        nsev_boundstates,
        nsev_discspec,
        nsev_D,
        nsev_q,
        nsev_T,
        nsev_kappa,
        ctypes.byref(options)
    )
    check_return_code(rv)
    rdict = {
        'return_value': rv,
        'q': nsev_q,
        'options': repr(options)
    }
    return rdict


def nsev_inverse_xi_wrapper(D, T1, T2, M, dis=None):
    """Helper function for nsev_inverse to calculate the spectral borders for a given time window.

    Return value is an array holding the position of the first and the last spectral
    sample to be used for nsev_inverse.

    Arguments:

    * D : number of sample points for the time window
    * T1, T2 : borders of the time window
    * M : number of samples for the continuous spectrum

    Optional Arguments:

    * dis : nse discretization parameter, default = 4

        * 0 = 2SPLIT2_MODAL
        * 1 = BO
        * 2 = 2SPLIT1A
        * 3 = 2SPLIT1B
        * 4 = 2SPLIT2A
        * 5 = 2SPLIT2B
        * 6 = 2SPLIT2S
        * 7 = 2SPLIT3A
        * 8 = 2SPLIT3B
        * 9 = 2SPLIT3S
        * 10 = 2SPLIT4A
        * 11 = 2SPLIT4B
        * 12 = 2SPLIT5A
        * 13 = 2SPLIT5B
        * 14 = 2SPLIT6A
        * 15 = 2SPLIT6B
        * 16 = 2SPLIT7A
        * 17 = 2SPLIT7B
        * 18 = 2SPLIT8A
        * 19 = 2SPLIT8B

    Returns:

    * rv : return value of the C-function
    * xi : two-element C double vector containing XI borders

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_nsev_inverse_xi_func = fnft_clib.fnft_nsev_inverse_XI
    clib_nsev_inverse_xi_func.restype = ctypes_int
    nsev_D = ctypes_uint(D)
    nsev_T = np.zeros(2, dtype=numpy_double)
    nsev_T[0] = T1
    nsev_T[1] = T2
    nsev_M = ctypes_uint(M)
    nsev_Xi = np.zeros(2, dtype=numpy_double)
    if dis is None:
        tmpoptions = get_nsev_inverse_options()
        dis = tmpoptions.discretization
    nsev_dis = ctypes_int32(dis)
    clib_nsev_inverse_xi_func.argtypes = [
        type(nsev_D),  # D
        np.ctypeslib.ndpointer(dtype=ctypes_double, ndim=1, flags='C'),  # t
        type(nsev_M),  # M
        np.ctypeslib.ndpointer(dtype=ctypes_double, ndim=1, flags='C'),  # xi
        type(nsev_dis)]
    rv = clib_nsev_inverse_xi_func(nsev_D, nsev_T, nsev_M, nsev_Xi, nsev_dis)
    return rv, nsev_Xi
