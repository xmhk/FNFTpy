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


import ctypes
import numpy as np

#
# data types for interfacing C
#
ctypes_int32 = ctypes.c_int32  # FNFT_INT, (C int32_t)
ctypes_uint = ctypes.c_size_t  # FNFT_UINT (C size_t)
ctypes_int = ctypes.c_int  # plain c integer, e.g. union elements
ctypes_double = ctypes.c_double  # FNFT_REAL
numpy_complex = np.complex128  # FNFT_COMPLEX for Arrays (C-double)
numpy_double = np.double  # FNFT_REAL for Arrays (C-double)


#
# option structs for interfacing C
#
class GenericOptionsStruct(ctypes.Structure):
    def __repr__(self):
        """return options as string, separated by commata"""
        s = ""
        for f in self._fields_:
            s+="%s : %s, "%(repr(f[0]), repr(self.__getattribute__(f[0])))
        return s[0:-2] #-2: drop the last comma

    def __str__(self):
        """return options as string, separated by newlines"""
        s = self.__repr__().replace(',','\n')
        return s


class KdvvOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_kdvv.

    Fields:

    * discretization

    """
    _fields_ = [
        ("discretization", ctypes_int)]



class NsepOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_nsep.

    Fields:

    * localization
    * filtering
    * bounding_box
    * max_evals
    * discretization
    * normalization_flag


    """
    _fields_ = [
        ("localization", ctypes_int),
        ("filtering", ctypes_int),
        ("bounding_box", ctypes_double * 4),
        ("max_evals", ctypes_uint),
        ("discretization", ctypes_int),
        ("normalization_flag", ctypes_int32)]

    def __repr__(self):
        s = "'localization' : " + repr(self.localization)
        s += ", 'filtering : " + repr(self.filtering)
        s += ", 'bounding box' : [" + repr(self.bounding_box[0]) + " " \
             + repr(self.bounding_box[1]) + " " + repr(self.bounding_box[2]) + " " \
             + repr(self.bounding_box[3])+"]"
        s += ", 'max_evals' : " + repr(self.max_evals)
        s += ", 'discretization' : " + repr(self.discretization)
        s += ", 'normalization_flag' : " + repr(self.normalization_flag)
        return s



class NsevOptionsStruct(GenericOptionsStruct):
    """Ctypes options struct for interfacing fnft_nsev.

    Fields:

    * bound_state_filtering
    * bound_state_localization
    * Dsub
    * niter
    * discspec_type
    * contspec_type
    * normalization_flag
    * discretization


        """
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),
        ("Dsub", ctypes_uint),
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int32),
        ("discretization", ctypes_int)]


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
    _fields_ = [
        ("discretization", ctypes_int),
        ("contspec_type", ctypes_int),
        ("contspec_inversion_method", ctypes_int),
        ("discspec_type", ctypes_int),
        ("max_iter", ctypes_uint),
        ("oversampling_factor", ctypes_uint)]





