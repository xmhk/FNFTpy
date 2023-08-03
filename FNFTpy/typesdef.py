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

Christoph Mahnke, 2018-2023

"""

import ctypes
import numpy as np
from enum import IntEnum

#
# data types for interfacing C
#
ctypes_int32 = ctypes.c_int32  # FNFT_INT, (C int32_t)
ctypes_uint = ctypes.c_size_t  # FNFT_UINT (C size_t)
ctypes_int = ctypes.c_int  # plain c integer, e.g. union elements
ctypes_double = ctypes.c_double  # FNFT_REAL
numpy_complex = np.complex128  # FNFT_COMPLEX for Arrays (C-double)
numpy_double = np.double  # FNFT_REAL for Arrays (C-double)
numpy_complex_arr_ptr = np.ctypeslib.ndpointer(dtype=numpy_complex,
                                               ndim=1, flags='C')  # pointer for C complex arrays
numpy_double_arr_ptr = np.ctypeslib.ndpointer(dtype=ctypes_double,
                                              ndim=1, flags='C')  # pointer for C double arrays

ctypes_nullptr = ctypes.POINTER(ctypes.c_int)()


#
# option structs for interfacing C
#
class GenericOptionsStruct(ctypes.Structure):
    """return options as string, separated by commata"""

    def __repr__(self):
        # make dummy c arrays: each array of a certain length is a different type
        dummy4 = (ctypes_double * 4)(0, 0, 0, 0)  # 4 item C array as reference
        dummy2 = (ctypes_double * 2)(0, 0)  # 4 item C array as reference
        s = ""
        for f in self._fields_:
            # ctype arrays don't have a readable repr of their contents ...
            # so they have to be handled differently
            if (f[1] == type(dummy4)) or (f[1] == type(dummy2)):
                tmps = "%s : [" % repr(f[0])
                for arritem in self.__getattribute__(f[0]):
                    tmps += repr(arritem) + " "
                s += tmps + "], "
            # standard case: c int / uint
            else:
                s += "%s : %s, " % (repr(f[0]), repr(self.__getattribute__(f[0])))
        return s[0:-2]  # -2: drop the last comma

    def __str__(self):
        """return options as string, separated by newlines"""
        s = self.__repr__().replace(',', '\n')
        return s

class KdvvOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_kdvv.

    Fields:

        * bound_state_localization
        * niter
        * discspec_type
        * contspec_type
        * normalization_flag
        * discretization
        * richardson_extrapolation_flag
        * grid_spacing
    """
    # note: order of fields here needs to be exactly as in .h file
    _fields_ = [
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),  # check uint
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int),  # check int
        ("discretization", ctypes_int),
        ("richardson_extrapolation_flag", ctypes_uint),
        ("grid_spacing", ctypes_double)  # check: uint
        ]


class ManakovvOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_manakovv.

    Fields:

        * bound_state_filtering
        * bound_state_localization
        * niter
        * Dsub
        * discspec_type
        * contspec_type
        * normalization_flag
        * discretization
        * richardson_extrapolation_flag

    * discretization
    """
    # note: order of fields here needs to be exactly as in .h file
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),  # check uint
        ("Dsub", ctypes_uint),  # check uint
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int),  # check int
        ("discretization", ctypes_int),
        ("richardson_extrapolation_flag", ctypes_uint)]  # check: uint

class NsepOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_nsep.

    Fields:

    * localization
    * filtering
    * bounding_box
    * max_evals
    * discretization
    * normalization_flag
    * floquet_range
    * points_per_spine
    * dsub
    * tol
    """
    # note: order of fields here needs to be exactly as in .h file
    _fields_ = [
        ("localization", ctypes_int),
        ("filtering", ctypes_int),
        ("bounding_box", ctypes_double * 4),
        ("max_evals", ctypes_uint),
        ("discretization", ctypes_int),
        ("normalization_flag", ctypes_int),
        ("floquet_range", ctypes_double * 2),
        ("points_per_spine", ctypes_uint),
        ("Dsub", ctypes_uint),
        ("tol", ctypes_double)
    ]


class NsevOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_nsev.

    Fields:

    * bound_state_filtering
    * bound_state_localization
    * Dsub
    * niter
    * tol
    * discspec_type
    * contspec_type
    * normalization_flag
    * discretization
    * richardson_extrapolation_flag
    * bounding box
    """
    # note: order of fields here needs to be exactly as in .h file
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),
        ("tol", ctypes_double),
        ("Dsub", ctypes_uint),
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int32),
        ("discretization", ctypes_int),
        ("richardson_extrapolation_flag", ctypes_int),
        ("bounding_box", ctypes_double * 4)]


class NsevInverseOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_nsev_inverse.

    Fields:

    * discretization
    * contspec_type
    * contspec_inversion_method
    * discspec_type
    * max_iter
    * oversampling_factor
    """
    # note: order of fields here needs to be exactly as in .h file
    _fields_ = [
        ("discretization", ctypes_int),
        ("contspec_type", ctypes_int),
        ("contspec_inversion_method", ctypes_int),
        ("discspec_type", ctypes_int),
        ("max_iter", ctypes_uint),
        ("oversampling_factor", ctypes_uint)]


# python enums
class fnft_nse_discretization(IntEnum):
    n2SPLIT2_MODAL = 0
    BO = 1
    n2SPLIT1A = 2
    n2SPLIT1B = 3
    n2SPLIT2A = 4
    n2SPLIT2B = 5
    n2SPLIT2S = 6
    n2SPLIT3A = 7
    n2SPLIT3B = 8
    n2SPLIT3S = 9
    n2SPLIT4A = 10
    n2SPLIT4B = 11
    n2SPLIT5A = 12
    n2SPLIT5B = 13
    n2SPLIT6A = 14
    n2SPLIT6B = 15
    n2SPLIT7A = 16
    n2SPLIT7B = 17
    n2SPLIT8A = 18
    n2SPLIT8B = 19
    n4SPLIT4A = 20
    n4SPLIT4B = 21
    CF4_2 = 22
    CF4_3 = 23
    CF5_3 = 24
    CF6_4 = 25
    ES4 = 26


class fnft_nsev_bsloc(IntEnum):
    FAST_EIGENVALUE = 0
    NEWTON = 1
    SUBSAMPLE_AND_REFINE = 2


class fnft_nsev_dstype(IntEnum):
    NORMING_CONSTANTS = 0
    RESIDUES = 1
    BOTH = 2


class fnft_nsev_cstype(IntEnum):
    REFLECTION_COEFFICIENT = 0
    AB = 1
    BOTH = 2


class fnft_kdvv_bsloc(IntEnum):
    NEWTON = 0
    GRIDSEARCH_AND_REFINE = 1


class fnft_kdvv_dstype(IntEnum):
    NORMING_CONSTANTS = 0
    RESIDUES = 1
    BOTH = 2


class fnft_kdvv_cstype(IntEnum):
    REFLECTION_COEFFICIENT = 0
    AB = 1
    BOTH = 2

class fnft_nsep_loc(IntEnum):
    SUBSAMPLE_AND_REFINE = 0
    NEWTON = 1
    GRIDSEARCH = 2
    MIXED = 3

class fnft_nsep_filt(IntEnum):
    NONE = 0
    MANUAL = 1
    AUTO = 2


class fnft_manakovv_dstype(IntEnum):
    NORMING_CONSTANTS = 0
    RESIDUES = 1
    BOTH = 2


class fnft_manakovv_cstype(IntEnum):
    REFLECTION_COEFFICIENT = 0
    AB = 1
    BOTH = 2


class fnft_manakovv_bsloc(IntEnum):
    FAST_EIGENVALUE = 0
    NEWTON = 1
    SUBSAMPLE_AND_REFINE = 2
