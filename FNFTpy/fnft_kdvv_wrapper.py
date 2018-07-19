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

Christoph Mahnke, 2018

"""


from .typesdef import *
from .options_handling import get_kdvv_options, print_kdvv_options
from .auxiliary import get_lib_path, check_return_code


def kdvv(u, tvec, M=128, Xi1=-2, Xi2=2, dis=None):
    """Calculate the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.

    This function is intended to be 'convenient', which means it
    automatically calculates some variables needed to call the
    C-library and uses some default options.
    Own options can be set by passing optional arguments (see below).

    Currently, only the contiuous spectrum is calculated.

    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more C-like interface is desired, the function 'kdvv_wrapper' can be used (see documentation there).

    Arguments:

        u : numpy array holding the samples of the field to be analyzed

        tvec : time vector

        M : number of samples for the continuous spectrum to calculate,


    Optional arguments:


        Xi1, Xi2 : min and max frequency for the continuous spectrum, default = [-2,2]

        dis : determines the discretization, default = 17

            0 = 2split1a
            1 = 2split1b
            2 = 2split2a
            3 = 2split2b
            4 = 2split2s
            5 = 2split3a
            6 = 2split3b
            7 = 2split3s
            8 = 2split4a
            9 = 2split4b
            10 = 2split5a
            11 = 2split5b
            12 = 2split6a
            13 = 2split6b
            14 = 2split7a
            15 = 2split7b
            16 = 2split8a
            17 = 2split8b


    Returns:

        rdict : dictionary holding the fields:

            return_value : return value from FNFT

            cont : continuous spectrum


    """

    D = len(u)
    K = 0  # not yet implemented
    T1 = np.min(tvec)
    T2 = np.max(tvec)
    options = get_kdvv_options(dis=dis)
    return kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                        K, options)


def kdvv_wrapper(D, u, T1, T2, M, Xi1, Xi2,
                 K, options):
    """Calculate the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries.

    This function's interface mimics the behavior of the function 'fnft_kdvv' of FNFT.
    It converts all Python input into the C equivalent and returns the result from FNFT.
    If a more simplified version is desired, 'kdvv' can be used (see documentation there).


    Currently, only the contiuous spectrum is calculated.

    Arguments:

        D : number of samples

        u : numpy array holding the samples of the field to be analyzed

        T1, T2  : time positions of the first and the last sample

        M : number of values for the continuous spectrum to calculate

        Xi1, Xi2 : min and max frequency for the continuous spectrum

        K : maximum number of bound states to calculate (no effect yet)

        options : options for kdvv as KdvvOptionsStruct. Can be generated e.g. with 'get_kdvv_options()'

    Returns:

        rdict : dictionary holding the fields:

            return_value : return value from FNFT

            cont : continuous spectrum

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
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
    # kdvv_k = ctypes_uint(k)
    # bound states -> will stay empty until implemented
    # kdvv_boundstates = np.zeros(k,dtype=numpy_complex)
    # discrete spectrum -> will stay empty until implemented
    # kdvv_discspec = np.zeros(k,dtype=numpy_complex)
    kdvv_nullptr = ctypes.POINTER(ctypes.c_int)()
    clib_kdvv_func.argtypes = [
        type(kdvv_D),  # D
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # u
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # t
        type(kdvv_M),  # M
        np.ctypeslib.ndpointer(dtype=numpy_complex,
                               ndim=1, flags='C'),  # cont
        np.ctypeslib.ndpointer(dtype=ctypes_double,
                               ndim=1, flags='C'),  # Xi
        type(kdvv_nullptr),  # K_ptr
        type(kdvv_nullptr),  # boundstates
        type(kdvv_nullptr),  # normconsts res
        ctypes.POINTER(KdvvOptionsStruct)]  # options ptr
    options.discretization=20
    rv = clib_kdvv_func(
        kdvv_D,
        kdvv_u,
        kdvv_T,
        kdvv_M,
        kdvv_cont,
        kdvv_Xi,
        kdvv_nullptr,
        kdvv_nullptr,
        kdvv_nullptr,
        ctypes.byref(options))
    check_return_code(rv)
    rdict = {'return_value': rv, 'cont': kdvv_cont, 'options':repr(options)}
    return rdict
