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


from .auxiliary import get_lib_path
from .typesdef import *


#
# Get and view options for kdvv (Korteweg-de Vries equation, vanishing boundaries)
#

def fnft_kdvv_default_options_wrapper():
    """Get the default options for kdvv directly from the FNFT C-library.

    Returns:

    * options : KdvvOptionsStruct with options for kdvv_wrapper

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_kdvv_default_opts
    clib_func.restype = KdvvOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_kdvv_options(options=None):
    """Print options of a KdvvOptionsStruct.

    When called without additional argument, the default options from FNFT are printed.

    Optional arguments:

    * options : KdvvOptionsStruct, e.g. created by get_kdvv_options()

    """
    if options is None:
        options = fnft_kdvv_default_options_wrapper()
    print(repr(options))


def get_kdvv_options(dis=None):
    """Get an KdvvOptionsStruct struct for use with kdvv_wrapper.

    When called without additional optional arguments, the default values from FNFT are used.

    Optional arguments:

    * dis: discretization, default = 17
        * 0 = 2split1a
        * 1 = 2split1b
        * 2 = 2split2a
        * 3 = 2split2b
        * 4 = 2split2s
        * 5 = 2split3a
        * 6 = 2split3b
        * 7 = 2split3s
        * 8 = 2split4a
        * 9 = 2split4b
        * 10 = 2split5a
        * 11 = 2split5b
        * 12 = 2split6a
        * 13 = 2split6b
        * 14 = 2split7a
        * 15 = 2split7b
        * 16 = 2split8a
        * 17 = 2split8b

    Returns:

    * options : KdvvOptionsStruct

    """
    options = fnft_kdvv_default_options_wrapper()
    if dis is not None:
        options.discretization = dis
    return options


#
#  Get and view options for nsep (Nonlinear Schroedinger equation, periodic boundaries)
#

def fnft_nsep_default_options_wrapper():
    """Get the default options for nsep directly from the FNFT C-library.

    Returns:

    * options : NsepOptionsStruct for nsep_wrapper

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsep_default_opts
    clib_func.restype = NsepOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsep_options(options=None):
    """Print options of a NsepOptionsStruct.

    When called without additional arguments, the default options from FNFT are printed.

    Optional arguments:

    * options : NsepOptionsStruct, e.g. created by get_nsep_options

    """
    if options is None:
        options = fnft_nsep_default_options_wrapper()
    print(repr(options))


def get_nsep_options(loc=None, filt=None, bb=None, maxev=None, dis=None, nf=None):
    """Get a NsepOptionsStruct struct for use with nsep_wrapper.

    When called without additional optional argument, the default values from FNFT are used.

    Optional arguments:

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

    * nf : normalization flag, default=1
        * 0 = off
        * 1 = on

    Returns:

    * options : NsepOptionsStruct

    """
    options = fnft_nsep_default_options_wrapper()
    if loc is not None:
        options.localization = loc
    if filt is not None:
        options.filtering = filt
    if nf is not None:
        options.normalization_flag = nf
    if dis is not None:
        options.discretization = dis
    if bb is not None:
        options.bounding_box[0] = bb[0]
        options.bounding_box[1] = bb[1]
        options.bounding_box[2] = bb[2]
        options.bounding_box[3] = bb[3]
    if maxev is not None:
        options.max_evals = maxev
    return options


#
#  Get and view options for nsep (Nonlinear Schroedinger equation, periodic boundaries)
#


def fnft_nsev_default_options_wrapper():
    """Get the default options for nsev directly from the FNFT C-library.

    Returns:

    * options : NsevOptionsStruct with options for nsev_wrapper

    """

    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsev_default_opts
    clib_func.restype = NsevOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsev_options(options=None):
    """Print options of a NsevOptionsStruct.

    When called without additional argument, the default options from FNFT are printed.

    Optional arguments:

    * options : NsevOptionsStruct, e.g. created by get_nsev_options()

    """

    if options is None:
        options = fnft_nsev_default_options_wrapper()
    print(repr(options))


def get_nsev_options(bsf=None, bsl=None, niter=None, Dsub=None, dst=None, cst=None, nf=None, dis=None):
    """Get a NsevOptionsStruct for use with nsev_wrapper.

    When called without additional optional arguments, the default values from FNFT are used.

    Optional arguments:

    * bsf : bound state filtering, default = 2
        * 0 = none
        * 1 = basic
        * 2 = full

    * bsl : bound state localization, default = 2
        * 0 = fast eigenvalue
        * 1 = Newton
        * 2 = subsample and refine

    * niter : number of iterations for Newton bound state location, default = 10
    * Dsub : number of samples used for 'subsampling and refine'-method, default = 0 (auto)
    * dst : type of discrete spectrum, default = 0
        * 0 = norming constants
        * 1 = residues
        * 2 = both

    * cst : type of continuous spectrum, default = 0
        * 0 = reflection coefficient
        * 1 = a and b
        * 2 = both

    * dis : discretization, default = 11
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

    * nf : normalization flag, default =  1
        * 0 = off
        * 1 = on

    Returns:

    * options : NsevOptionsStruct

    """
    options = fnft_nsev_default_options_wrapper()
    if bsf is not None:
        options.bound_state_filtering = bsf
    if bsl is not None:
        options.bound_state_localization = bsl
    if niter is not None:
        options.niter = niter
    if Dsub is not None:
        options.Dsub = Dsub
    if dst is not None:
        options.discspec_type = dst
    if cst is not None:
        options.contspec_type = cst
    if nf is not None:
        options.normalization_flag = nf
    if dis is not None:
        options.discretization = dis
    return options


def fnft_nsev_inverse_default_options_wrapper():
    """Get the default options for nsev_inverse directly from the FNFT C-library.

    Returns:

    * options : NsevInverseOptionsStruct with options for nsev_inverse_wrapper

    """

    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsev_inverse_default_opts
    clib_func.restype = NsevInverseOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsev_inverse_options(options=None):
    """Print options of a NsevInverseOptionsStruct for nsev_inverse.

    When called without additional argument, the default options from FNFT are printed.

    Optional arguments:

    * options : NsevInverseOptionsStruct, e.g. created by get_nsev_options()
    """

    if options is None:
        options = fnft_nsev_inverse_default_options_wrapper()
    print(repr(options))


def get_nsev_inverse_options(dis=None, cst=None, csim=None, dst=None, max_iter=None, osf=None):
    """Get a NsevInverseOptionsStruct for use with nsev_inverse_wrapper.

    When called without additional optional arguments, the default values from FNFT are used.

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

    Returns:

    * options : NsevInverseOptionsStruct

    """
    options = fnft_nsev_inverse_default_options_wrapper()
    if dis is not None:
        options.discretization = dis
    if cst is not None:
        options.contspec_type = cst
    if csim is not None:
        options.contspec_inversion_method = csim
    if dst is not None:
        options.discspec_type = dst
    if max_iter is not None:
        options.max_iter = max_iter
    if osf is not None:
        options.oversampling_factor = osf
    return options




