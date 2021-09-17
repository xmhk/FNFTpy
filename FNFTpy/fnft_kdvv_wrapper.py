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

Christoph Mahnke, 2018, 2019

"""

from .typesdef import *
from .options_handling import get_kdvv_options
from .auxiliary import get_lib_path, check_return_code, get_winmode_param


def kdvv(u, tvec, M=128, Xi1=-2, Xi2=2, dis=None, bsl=None, bsf=None, niter=None, dst=None, cst=None, nf=None,
                     ref=None, bound_state_guesses=None):
    """Calculate the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.

    This function is intended to be 'convenient', which means it
    automatically calculates some variables needed to call the
    C-library and uses some default options.
    Own options can be set by passing optional arguments (see below).

    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'kdvv_wrapper' can be used (see documentation there).

    Arguments:

    * u : numpy array holding the samples of the field to be analyzed
    * tvec : time vector

    Optional arguments:

    * M : number of samples for the continuous spectrum to calculate, default = 128

    * Xi1, Xi2 : min and max frequency for the continuous spectrum, default = [-2,2]

    * dis: discretization, default = 17  (for details see FNFT documentation)  TODO update

         * 0 = 2SPLIT1A
         * 1 = 2SPLIT1B
         * 2 = 2SPLIT2A
         * 3 = 2SPLIT2B
         * 4 = 2SPLIT2S
         * 5 = 2SPLIT3A
         * 6 = 2SPLIT3B
         * 7 = 2SPLIT3S
         * 8 = 2SPLIT4A
         * 9 = 2SPLIT4B
         * 10 = 2SPLIT5A
         * 11 = 2SPLIT5B
         * 12 = 2SPLIT6A
         * 13 = 2SPLIT6B
         * 14 = 2SPLIT7A
         * 15 = 2SPLIT7B
         * 16 = 2SPLIT8A
         * 17 = 2SPLIT8B
         * 18 = 4SPLIT4A
         * 19 = 4SPLIT4B
         * 20 = BO
         * 21 = CF4_2
         * 22 = CF4_3
         * 23 = CF5_3
         * 24 = CF6_4

    * bsl: bound state localization, default=1
        * NEWTON,
        * GRIDSEARCH_AND_REFINE

    * bsf: bound state filtering, default=1
        * 0 = NEWTON,
        * 1 = GRIDSEARCH_AND_REFINE

    * niter : number of iterations for Newton bound state location, default = 10

    * dst : type of discrete spectrum, default = 0
        * 0 = norming constants
        * 1 = residues
        * 2 = both
        * 3 = skip computing discrete spectrum

   * cst : type of continuous spectrum, default = 0
        * 0 = reflection coefficient
        * 1 = a and b
        * 2 = both
        * 3 = skip computing continuous spectrum TODO: implement

   * nf : normalization flag, default =  1
       * 0 = off
       * 1 = on

   * ref : richardson extrapolation flag, default = 0
        * 0 = off
        * 1 = on


    Returns:

   * rdict : dictionary holding the fields:

       * return_value : return value from FNFT
       * cont_ref : continuous spectrum (reflection)
       * bound_states_num : number of bound states found
       * bound_states : array of bound states found
       * disc_norm : discrete spectrum - norming constants
       * disc_res : discrete spectrum - residues
       * cont_ref : continuous spectrum - reflection coefficient
       * cont_a : continuous spectrum - scattering coefficient a
       * cont_b : continuous spectrum - scattering coefficient b
       * options : KdvvOptionsStruct with options used

    """

    D = len(u)
    K = 0  # not yet implemented
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_kdvv_options(dis=dis, bsl=bsl, bsf=bsf, niter=niter, dst=dst, cst=cst, nf=nf,
                     ref=ref)
    return kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                        K, options, bound_state_guesses=bound_state_guesses)


def kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                 K, options, bound_state_guesses=None):
    """Calculate the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.

    This function's interface mimics the behavior of the function 'fnft_kdvv' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'kdvv' can be used (see documentation there).

    Arguments:

    * D : number of samples
    * u : numpy array holding the samples of the field to be analyzed
    * T1, T2  : time positions of the first and the last sample
    * M : number of values for the continuous spectrum to calculate
    * Xi1, Xi2 : min and max frequency for the continuous spectrum
    * K : maximum number of bound states to calculate
    * options : options for kdvv as KdvvOptionsStruct. Can be generated e.g. with 'get_kdvv_options()'

    Optional Arguments:

    * bound_state_guesses: list or array of bound state guesses, only effective if bsl==1 (Newton
                         bound state location is activated). Default = None

    Returns:

    * rdict : dictionary holding the fields:

        * return_value : return value from FNFT
        * cont_ref : continuous spectrum (reflection)
        * bound_states_num : number of bound states found
        * bound_states : array of bound states found
        * disc_norm : discrete spectrum - norming constants
        * disc_res : discrete spectrum - residues
        * cont_ref : continuous spectrum - reflection coefficient
        * cont_a : continuous spectrum - scattering coefficient a
        * cont_b : continuous spectrum - scattering coefficient b
        * options : KdvvOptionsStruct with options used
    """
    fnft_clib = ctypes.CDLL(get_lib_path(), winmode = get_winmode_param())
    clib_kdvv_func = fnft_clib.fnft_kdvv
    clib_kdvv_func.restype = ctypes_int
    kdvv_D = ctypes_uint(D)
    kdvv_u = np.zeros(kdvv_D.value, dtype=numpy_complex)
    kdvv_u[:] = u[:] + 0.0j
    kdvv_T = np.zeros(2, dtype=numpy_double)
    kdvv_T[0] = T1
    kdvv_T[1] = T2
    kdvv_M = ctypes_uint(M)
    kdvv_cont = np.zeros(M, dtype=numpy_complex)
    kdvv_Xi = np.zeros(2, dtype=numpy_double)
    kdvv_Xi[0] = Xi1
    kdvv_Xi[1] = Xi2
    kdvv_K = ctypes_uint(K)

    #
    # discrete spectrum -> reflection coefficient and / or residues
    #
    kdvv_bound_states_type = numpy_complex_arr_ptr
    kdvv_disc_spec_type = numpy_complex_arr_ptr
    if (options.discspec_type == 0) or (options.discspec_type == 1):
        # norming consts OR residues
        kdvv_discspec = np.zeros(K, dtype=numpy_complex)
        kdvv_boundstates = np.zeros(K, dtype=numpy_complex)
    elif options.discspec_type == 2:
        # norming consts AND res
        kdvv_discspec = np.zeros(2 * K, dtype=numpy_complex)
        kdvv_boundstates = np.zeros(K, dtype=numpy_complex)
    else: #no discrete spectrum
        kdvv_discspec = ctypes_nullptr
        kdvv_boundstates = ctypes_nullptr
        kdvv_bound_states_type = type(ctypes_nullptr)
        kdvv_disc_spec_type = type(ctypes_nullptr)

    #
    # for Newton refinement: use guesses, if provided.
    #
    if options.bound_state_localization == 0:
        if bound_state_guesses is not None:
            bsg_copy = np.array(bound_state_guesses, dtype=np.complex128)
            if len(bsg_copy) > 0:
                ii = -1
                # copy as many of the guesses to bound state array
                while (ii < K - 1) and (ii < len(bsg_copy) - 1) and (ii < len(kdvv_boundstates) - 1):
                    ii = ii + 1
                    kdvv_boundstates[ii] = bsg_copy[ii]


    #
    # continuous spectrum -> reflection coefficient and / or a,b
    #
    kdvv_cont_spec_type = numpy_complex_arr_ptr
    if options.contspec_type == 0:
        # reflection coeff.
        kdvv_cont = np.zeros(kdvv_M.value, dtype=numpy_complex)
    elif options.contspec_type == 1:
        # a and b
        kdvv_cont = np.zeros(2 * kdvv_M.value, dtype=numpy_complex)
    elif options.contspec_type == 2:
        # a and b AND reflection coeff.
        kdvv_cont = np.zeros(3 * kdvv_M.value, dtype=numpy_complex)
    else:
        # 3 or any other option: skip continuous spectrum -> pass NULL
        kdvv_cont = ctypes_nullptr
        kdvv_cont_spec_type = type(ctypes_nullptr)

    clib_kdvv_func.argtypes = [
        type(kdvv_D),  # D
        numpy_complex_arr_ptr,  # u
        numpy_double_arr_ptr,  # t
        type(kdvv_M),  # M
        kdvv_cont_spec_type,  # cont
        numpy_double_arr_ptr,  # Xi
        ctypes.POINTER(ctypes_uint),  # K_ptr
        kdvv_bound_states_type,#numpy_complex_arr_ptr,  # boundstates
        kdvv_disc_spec_type,  # normconsts res
        ctypes.POINTER(KdvvOptionsStruct)]  # options ptr
    rv = clib_kdvv_func(
        kdvv_D,
        kdvv_u,
        kdvv_T,
        kdvv_M,
        kdvv_cont,
        kdvv_Xi,
        kdvv_K,
        kdvv_boundstates,
        kdvv_discspec,
        ctypes.byref(options))
    check_return_code(rv)
    K_new = kdvv_K.value  #number of bound states found
    # print(type(int(kdvv_k.value))) # TODO needs to be cleaned, cases?
    rdict = {'return_value': rv,
             'bound_states_num': K_new,
             'bound_states': kdvv_boundstates[0:K_new],
             'options': repr(options)}
    #
    # depending on options: output of discrete spectrum
    #
    if options.discspec_type == 0:
        # norming const
        rdict['disc_norm'] = kdvv_discspec[0:K_new]
    elif options.discspec_type == 1:
        # residues
        rdict['disc_res'] = kdvv_discspec[0:K_new]
    elif options.discspec_type == 2:
        # norming const. AND residues
        rdict['disc_norm'] = kdvv_discspec[0:K_new]
        rdict['disc_res'] = kdvv_discspec[K_new:2 * K_new]
    else:
        # no discrete spectrum calculated
        pass
    #
    # depending on options: output of continuous spectrum
    #
    if options.contspec_type == 0:
        # refl. coeff
        rdict['cont_ref'] = kdvv_cont[0:M]
    elif options.contspec_type == 1:
        # a and b
        rdict['cont_a'] = kdvv_cont[0:M]
        rdict['cont_b'] = kdvv_cont[M:2 * M]
    elif options.contspec_type == 2:
        # refl. coeff AND a and b
        rdict['cont_ref'] = kdvv_cont[0:M]
        rdict['cont_a'] = kdvv_cont[M:2 * M]
        rdict['cont_b'] = kdvv_cont[2 * M:3 * M]
    else:
        # no cont. spectrum calculated
        pass
    return rdict
