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
class KdvvOptionsStruct(ctypes.Structure):
    """Ctypes options struct for interfacing fnft_kdvv"""
    _fields_ = [
        ("discretization", ctypes_int)]

    def __repr__(self):
        s = "  discretization : dis " + repr(self.discretization)
        return s


class NsepOptionsStruct(ctypes.Structure):
    """Ctypes options struct for interfacing fnft_nsep"""
    _fields_ = [
        ("localization", ctypes_int),
        ("filtering", ctypes_int),
        ("bounding_box", ctypes_double * 4),
        ("max_evals", ctypes_uint),
        ("discretization", ctypes_int),
        ("normalization_flag", ctypes_int32)]

    def __repr__(self):
        s = "  localization                  : loc   " + repr(self.localization)
        s += "\n   filtering                     : filt  " + repr(self.filtering)
        s += "\n   bounding box                  : bb    " + repr(self.bounding_box[0]) + " " \
             + repr(self.bounding_box[1]) + " " + repr(self.bounding_box[2]) + " " \
             + repr(self.bounding_box[3])
        s += "\n   maximum number of evaluations : maxev " + repr(self.max_evals)
        s += "\n   discretization                : dis   " + repr(self.discretization)
        s += "\n   normalization flag            : nf    " + repr(self.normalization_flag)
        return s


class NsevOptionsStruct(ctypes.Structure):
    """Ctypes options struct for interfacing fnft_kdvv"""
    _fields_ = [
        ("bound_state_filtering", ctypes_int),
        ("bound_state_localization", ctypes_int),
        ("niter", ctypes_uint),
        ("discspec_type", ctypes_int),
        ("contspec_type", ctypes_int),
        ("normalization_flag", ctypes_int32),
        ("discretization", ctypes_int)]

    def __repr__(self):
        s = "  bound state filtering    : bsf " + repr(self.bound_state_filtering)
        s += "\n   bound state localization : bsl " + repr(self.bound_state_localization)
        s += "\n   number of iteratons      : niter " + repr(self.niter)
        s += "\n   discrete spectrum type   : dst " + repr(self.discspec_type)
        s += "\n   continuous spectrum type : cst " + repr(self.contspec_type)
        s += "\n   discretization           : dis " + repr(self.discretization)
        s += "\n   normalization flag       : nf " + repr(self.normalization_flag)
        return s
