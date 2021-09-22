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

Christoph Mahnke 2021

"""


from .typesdef import *
from .auxiliary import get_lib_path, check_return_code, get_winmode_param
from .options_handling import get_manakovv_options


def manakovv(q1, q2, tvec, Xi1=-1.75, Xi2=2, M=128, K=128, kappa=1, bsf=None,
         bsl=None, niter=None, Dsub=None, dst=None, cst=None, nf=None, dis=None, ref=None,
         ):
    """
    TODO write Documentation
    :param q1:
    :param q2:
    :param tvec:
    :param Xi1:
    :param Xi2:
    :param M:
    :param K:
    :param kappa:
    :param bsf:
    :param bsl:
    :param niter:
    :param Dsub:
    :param dst:
    :param cst:
    :param nf:
    :param dis:
    :param ref:
    :return:
    """

    D = len(q1)
    if len(q1) != len(q2):
        print("Warning: q1 and q2 should be of same length.")
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_manakovv_options(bsf=bsf, bsl=bsl, niter=niter, Dsub=Dsub, dst=dst, cst=cst, nf=nf, dis=dis, ref=ref)
    return manakovv_wrapper(D, q1, q2, T1, T2, Xi1, Xi2,
                        M, K, kappa, options)


def manakovv_wrapper(D, q1, q2, T1, T2, Xi1, Xi2, M, K, kappa, options  ):
    fnft_clib = ctypes.CDLL(get_lib_path(), winmode=get_winmode_param())
    clib_manakovv_func = fnft_clib.fnft_manakovv
    clib_manakovv_func.restype = ctypes_int
    manakovv_D = ctypes_uint(D)
    manakovv_M = ctypes_uint(M)
    manakovv_K = ctypes_uint(K)
    manakovv_T = np.zeros(2, dtype=numpy_double)
    manakovv_T[0] = T1
    manakovv_T[1] = T2
    manakovv_q1 = np.zeros(manakovv_D.value, dtype=numpy_complex)
    manakovv_q2 = np.zeros(manakovv_D.value, dtype=numpy_complex)
    manakovv_q1[:] = q1[:] + 0.0j
    manakovv_q2[:] = q2[:] + 0.0j
    manakovv_kappa = ctypes_int(kappa)
    manakovv_Xi = np.zeros(2, dtype=numpy_double)
    manakovv_Xi[0] = Xi1
    manakovv_Xi[1] = Xi2
    #
    # discrete spectrum -> reflection coefficient and / or residues
    #
    manakovv_bound_states_type = numpy_complex_arr_ptr
    manakovv_disc_spec_type = numpy_complex_arr_ptr
    if (options.discspec_type == fnft_manakovv_dstype.NORMING_CONSTANTS)\
            or (options.discspec_type == fnft_manakovv_dstype.RESIDUES):
        manakovv_discspec = np.zeros(K, dtype=numpy_complex)    # todo check sizes
        manakovv_boundstates = np.zeros(K, dtype=numpy_complex)
    elif options.discspec_type == fnft_manakovv_dstype.BOTH:
        manakovv_discspec = np.zeros(2 * K, dtype=numpy_complex)  # todo check sizes
        manakovv_boundstates = np.zeros(K, dtype=numpy_complex)
    else:
        # 3 or any other option: skip discrete spec -> pass NULL
        manakovv_discspec = ctypes_nullptr
        manakovv_boundstates = ctypes_nullptr
        manakovv_bound_states_type = type(ctypes_nullptr)
        manakovv_disc_spec_type = type(ctypes_nullptr)
    #
    # for Newton refinement: use guesses, if provided.
    #
    if options.bound_state_localization == 1:
        pass
        # todo : implement
    #
    # continuous spectrum -> reflection coefficient and / or a,b
    #
    manakovv_cont_spec_type = numpy_complex_arr_ptr

    if options.contspec_type == fnft_manakovv_cstype.REFLECTION_COEFFICIENT:   # this is default
        manakovv_cont = np.zeros(2 * M, dtype=numpy_complex)
    elif options.contspec_type == fnft_manakovv_cstype.AB:
        manakovv_cont = np.zeros(3 * M, dtype=numpy_complex)
    elif options.contspec_type == fnft_manakovv_cstype.BOTH:
        manakovv_cont = np.zeros(5 * M, dtype=numpy_complex)
    else:
        # 3 or any other option: skip continuous spectrum -> pass NULL
        manakovv_cont = ctypes_nullptr
        manakovv_cont_spec_type = type(ctypes_nullptr)

    clib_manakovv_func.argtypes = [
        type(manakovv_D),  # D
        numpy_complex_arr_ptr,  # q1
        numpy_complex_arr_ptr,  # q2
        numpy_double_arr_ptr,  # t
        type(manakovv_M),  # M
        manakovv_cont_spec_type,  # cont
        numpy_double_arr_ptr,  # xi
        ctypes.POINTER(ctypes_uint),  # K_ptr
        manakovv_bound_states_type,  # boundstates
        manakovv_disc_spec_type,  # normconst res
        type(manakovv_kappa),  # kappa
        ctypes.POINTER(ManakovvOptionsStruct)]  # options ptr

    rv = clib_manakovv_func(
        manakovv_D,
        manakovv_q1,
        manakovv_q2,
        manakovv_T,
        manakovv_M,
        manakovv_cont,
        manakovv_Xi,
        manakovv_K,
        manakovv_boundstates,
        manakovv_discspec,
        manakovv_kappa,
        ctypes.byref(options))
    check_return_code(rv)
    K_new = manakovv_K.value
    rdict = {
        'return_value': rv,
        'bound_states_num': K_new,
        'bound_states': manakovv_boundstates[0:K_new]}
    #
    # depending on options: output of discrete spectrum
    #
    if options.discspec_type == fnft_manakovv_dstype.NORMING_CONSTANTS:
        rdict['disc_norm'] = manakovv_discspec[0:K_new]
    elif options.discspec_type == fnft_manakovv_dstype.RESIDUES:
        rdict['disc_res'] = manakovv_discspec[0:K_new]
    elif options.discspec_type == fnft_manakovv_dstype.BOTH:
        rdict['disc_norm'] = manakovv_discspec[0:K_new]
        rdict['disc_res'] = manakovv_discspec[K_new:2 * K_new]
    else:
        # no discrete spectrum calculated
        pass
    #
    # depending on options: output of continuous spectrum
    #
    if options.contspec_type == fnft_manakovv_cstype.REFLECTION_COEFFICIENT:
        rdict['cont_ref1'] = manakovv_cont[0:M]
        rdict['cont_ref2'] = manakovv_cont[M:2*M]
    if options.contspec_type == fnft_manakovv_cstype.AB:
        # a and b
        rdict['cont_a'] = manakovv_cont[0:M]
        rdict['cont_b1'] = manakovv_cont[M:2*M]
        rdict['cont_b2'] = manakovv_cont[2*M::]
    if options.contspec_type == fnft_manakovv_cstype.BOTH:
        rdict['cont_ref1'] = manakovv_cont[0:M]
        rdict['cont_ref2'] = manakovv_cont[M:2 * M]
        rdict['cont_a'] = manakovv_cont[2*M:3*M]
        rdict['cont_b1'] = manakovv_cont[3*M:4*M]
        rdict['cont_b2'] = manakovv_cont[4*M::]
    rdict['options'] = repr(options)
    return rdict