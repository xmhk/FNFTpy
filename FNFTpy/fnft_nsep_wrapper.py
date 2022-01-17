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

Christoph Mahnke, 2018-2020

"""

from .typesdef import *
from .auxiliary import get_lib_path, check_return_code, get_winmode_param
from .options_handling import print_nsep_options, get_nsep_options


def nsep(q, T1, T2, kappa=1, loc=None, filt=None, bb=None,
         maxev=None, dis=None, nf=None, floq_range=None, ppspine=None, dsub=None, tol=None, phase_shift=0.0,
         display_c_msg=True):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with periodic boundaries.

    This function is intended to be 'convenient', which means it
    automatically calculates some variables needed to call the
    C-library and uses some default options.
    Own options can be set by passing optional arguments (see below).
    Options can be set by passing optional arguments (see below).

    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'nsep_wrapper' can be used (see documentation there).

    Arguments:

    * q : numpy array holding the samples of the input field
    * T1, T2  : time positions of the first and the (D+1) sample, where D is the number of samples

    Optional arguments:

    * kappa : +/- 1 for focussing/defocussing nonlinearity, default = 1
    * loc : localization method for the spectrum, default = 2

        * 0 = subsample and refine
        * 1 = gridsearch
        * 2 = mixed

    * filt : filtering of spectrum, default = 2

        * 0 = none
        * 1 = manual
        * 2 = auto

    * bb: bounding box used for manual filtering, default = [-inf, inf, -inf, inf]
    * maxev : maximum number of evaluations for root refinement, default = 20
    * nf : normalization flag default = 1

        * 0 = off
        * 1 = on

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
         * 20 = 4SPLIT4A
         * 21 = 4SPLIT4B
         * 22 = CF4_2
         * 23 = CF4_3
         * 24 = CF5_3
         * 25 = CF6_4
         * 26 = ES4
         * 27 = TES4

    * nf : normalization flag, default=1

        * 0 = off
        * 1 = on

    * floq_range : array of two reals defining Floquet range, default = [-1, 1]

    * ppspin : points per spine: defining the grid between interval set by floq_range

    * dsub : approximate number of samples for 'subsample and refine' localization

    * tol : Tolerance, for root search refinement. Can be either positibe number or (default =-1 (=auto))

    * phase_shift :  change of the phase over one quasi-period, arg(q(t+(T2-T1)/q(t)) (default=0)

    * display_c_msg : whether or not to show messages raised by the C-library, default = True


    Returns:

    * rdict : dictionary holding the fields (depending on options)

        * return_value : return value from FNFT
        * K : number of points in the main spectrum
        * main : main spectrum
        * M: number of points in the auxiliary spectrum
        * aux: auxiliary spectrum
        * options : NsepOptionsStruct with options used

        """
    D = len(q)
    options = get_nsep_options(loc=loc, filt=filt, bb=bb, maxev=maxev, dis=dis, nf=nf,
                               floq_range=floq_range, ppspine=ppspine, dsub=dsub, tol=tol)
    return nsep_wrapper(D, q, T1, T2, phase_shift,
                        kappa, options, display_c_msg=display_c_msg)


def nsep_wrapper(D, q, T1, T2, phase_shift, kappa,
                 options, display_c_msg=True):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with periodic boundaries.

    This function's interface mimics the behavior of the function 'fnft_nsep' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'nsep' can be used (see documentation there).

    Arguments:

    * D : number of sample points
    * q : numpy array holding the samples of the input field
    * T1, T2  : time positions of the first and the (D+1) sample
    * phase_shift : change of the phase over one quasi-period, arg(q(t+(T2-T1)/q(t))
    * kappa   : +/- 1 for focussing/defocussing nonlinearity
    * options : options for nsep as NsepOptionsStruct. Can be generated e.g. with 'get_nsep_options()'

    Optional Arguments:

    * display_c_msg : whether or not to show messages raised by the C-library, default = True

    Returns:

    * rdict : dictionary holding the fields (depending on options)

        * return_value : return value from FNFT
        * K : number of points in the main spectrum
        * main : main spectrum
        * M: number of points in the auxiliary spectrum
        * aux: auxiliary spectrum
        * options : NsepOptionsStruct with options used

    """

    fnft_clib = ctypes.CDLL(get_lib_path(), winmode=get_winmode_param())
    clib_nsep_func = fnft_clib.fnft_nsep
    clib_nsep_func.restype = ctypes_int
    if not display_c_msg:  # suppress output from C-library
        clib_errwarn_setprintf = fnft_clib.fnft_errwarn_setprintf
        clib_errwarn_setprintf(ctypes_nullptr)
    nsep_D = ctypes_uint(D)
    nsep_q = np.zeros(nsep_D.value, dtype=numpy_complex)
    nsep_q[:] = q[:] + 0.0j
    nsep_T = np.zeros(2, dtype=numpy_double)
    nsep_T[0] = T1
    nsep_T[1] = T2
    nsep_phase_shift = ctypes_double(phase_shift)
    nsep_K = ctypes_uint(4 * nsep_D.value)
    nsep_main_spec = np.zeros(nsep_K.value, dtype=numpy_complex)
    nsep_M = ctypes_uint(2 * nsep_D.value)
    nsep_aux_spec = np.zeros(nsep_M.value, dtype=numpy_complex)
    nsep_sheet_indices = ctypes_nullptr
    nsep_kappa = ctypes_int(kappa)

    clib_nsep_func.argtypes = [
        type(nsep_D),  # D
        numpy_complex_arr_ptr,  # q
        numpy_double_arr_ptr,  # t
        type(nsep_phase_shift),  # phase_shift
        ctypes.POINTER(ctypes_uint),  # K_ptr
        numpy_complex_arr_ptr,  # main_spec
        ctypes.POINTER(ctypes_uint),  # M_ptr
        numpy_complex_arr_ptr,  # aux_spec
        type(nsep_sheet_indices),  # sheet indices
        type(nsep_kappa),  # kappa
        ctypes.POINTER(NsepOptionsStruct)]  # options ptr

    rv = clib_nsep_func(
        nsep_D,
        nsep_q,
        nsep_T,
        nsep_phase_shift,
        nsep_K,
        nsep_main_spec,
        nsep_M,
        nsep_aux_spec,
        nsep_sheet_indices,
        nsep_kappa,
        ctypes.byref(options))
    check_return_code(rv)
    rdict = {
        'return_value': rv,
        'K': nsep_K.value,
        'main': nsep_main_spec[0:nsep_K.value],
        'M': nsep_M.value,
        'aux': nsep_aux_spec[0:nsep_M.value],
        'options': repr(options)}
    return rdict
