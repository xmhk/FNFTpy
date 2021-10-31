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


def nsep(q, T1, T2, K=None, M=None, kappa=1, loc=None, filt=None, bb=None,
         maxev=None, dis=None, nf=None, floq_range=None, ppspine=None, dsub=None, tol=None, phase_shift=0.0):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with periodic boundaries.

    This function is intended to be 'convenient', which means it
    automatically calculates some variables needed to call the
    C-library and uses some default options.
    Own options can be set by passing optional arguments (see below).

    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'nsep_wrapper' can be used (see documentation there).

    Arguments:

    * q : numpy array holding the samples of the input field (lenght should be a power of two)
    * T1, T2  : time positions of the first and the (D+1) sample, where D is the number of samples

    Optional arguments:

    * K : guess for the numbers of points for the main spectrum.
          If omitted K=D * options.points_per_spine will be used
    * M : guess for the numbers of points for the auxiliary specrum.
          If omitted M=D
    * kappa : +/- 1 for focussing/defocussing nonlinearity, default = 1
    * loc : localization method for the spectrum, default = 2

        - SUBSAMPLE_AND_REFINE = 0
        - NEWTON = 1
        - GRIDSEARCH = 2
        - MIXED = 3

    * filt : filtering of spectrum, default = 2

            - NONE = 0
            - MANUAL = 1
            - AUTO = 2

    * bb: bounding box used for manual filtering, default = [-inf, inf, -inf, inf]
    * maxev : maximum number of evaluations for root refinement, default = 20
    * dis : discretization, default = 4

        - 0 = 2SPLIT2_MODAL
        - 1 = BO
        - 2 = 2SPLIT1A
        - 4 = 2SPLIT2A
        - 5 = 2SPLIT2B
        - 6 = 2SPLIT2S
        - 7 = 2SPLIT3A
        - 8 = 2SPLIT3B
        - 9 = 2SPLIT3S
        - 10 = 2SPLIT4A
        - 11 = 2SPLIT4B
        - 12 = 2SPLIT5A
        - 13 = 2SPLIT5B
        - 14 = 2SPLIT6A
        - 15 = 2SPLIT6B
        - 16 = 2SPLIT7A
        - 17 = 2SPLIT7B
        - 18 = 2SPLIT8A
        - 19 = 2SPLIT8B
        - 20 = 4SPLIT4A
        - 21 = 4SPLIT4B
        - 22 = CF4_2
        - 23 = CF4_3
        - 24 = CF5_3
        - 25 = CF6_4
        - 26 = ES4
        - 27 = TES4

    * nf : normalization flag, default=1

        * 0 = off
        * 1 = on

    * floq_range : array of two reals defining Floquet range, default = [-1, 1]

    * ppspine : points per spine: defining the grid between interval set by floq_range

    * dsub : approximate number of samples for 'subsample and refine' localization

    * tol : Tolerance, for root search refinement. Can be either positibe number or (default =-1 (=auto))

    * phase_shift :  change of the phase over one quasi-period, arg(q(t+(T2-T1)/q(t)) (default=0)

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
    if K is None:
        K = options.points_per_spine * D
    if M is None:
        M = D
    return nsep_wrapper(D, q, T1, T2, K, M, phase_shift,
                        kappa, options)


def nsep_wrapper(D, q, T1, T2, K, M, phase_shift, kappa,
                 options):
    """Calculate the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with periodic boundaries.

    This function's interface mimics the behavior of the function 'fnft_nsep' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'nsep' can be used (see documentation there).

    Arguments:

    * D : number of sample points (should be power of 2)
    * q : numpy array holding the samples of the input field
    * T1, T2  : time positions of the first and the (D+1) sample
    * K : expected length of the main spectrum. A good guess is options.points_per_spine * D
    * M : expected length of the auxiliary specrum. A good guess is D
    * phase_shift : change of the phase over one quasi-period, arg(q(t+(T2-T1)/q(t))
    * kappa   : +/- 1 for focussing/defocussing nonlinearity
    * options : options for nsep as NsepOptionsStruct. Can be generated e.g. with 'get_nsep_options()'

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
    nsep_D = ctypes_uint(D)
    nsep_K = ctypes_uint(K)
    nsep_M = ctypes_uint(M)
    nsep_q = np.zeros(nsep_D.value, dtype=numpy_complex)
    nsep_q[:] = q[:] + 0.0j
    nsep_T = np.zeros(2, dtype=numpy_double)
    nsep_T[0] = T1
    nsep_T[1] = T2
    nsep_phase_shift = ctypes_double(phase_shift)
    #nsep_K = ctypes_uint(4 * nsep_D.value)
    #nsep_K = ctypes_uint(options.points_per_spine * nsep_D.value)
    nsep_main_spec = np.zeros(nsep_K.value, dtype=numpy_complex)
    #nsep_M = ctypes_uint(1 * nsep_D.value)
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
