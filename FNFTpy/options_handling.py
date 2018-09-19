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

def fnft_kdvv_default_opts_wrapper():
    """Get the default options for kdvv directly from the FNFT C-library.

    Returns:

        options : KdvvOptionsStruct with options for kdvv_wrapper

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_kdvv_default_opts
    clib_func.restype = KdvvOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_kdvv_options(opts=None):
    """Print options of a KdvvOptionsStruct.

    When called without additional argument, the default options from FNFT are printed.

    Optional arguments:

        opts : KdvvOptionsStruct, e.g. created by get_kdvv_options()

    """
    if opts is None:
        opts = fnft_kdvv_default_opts_wrapper()
    print(repr(opts))


def get_kdvv_options(dis=None):
    """Get an KdvvOptionsStruct struct for use with kdvv_wrapper.

    When called without additional optional arguments, the default values from FNFT are used.

    Optional arguments:

        dis: discretization, default = 17

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

        options : KdvvOptionsStruct

    """
    opts = fnft_kdvv_default_opts_wrapper()
    if dis is not None:
        opts.discretization = dis
    return opts


#
#  Get and view options for nsep (Nonlinear Schroedinger equation, periodic boundaries)
#

def fnft_nsep_default_opts_wrapper():
    """Get the default options for nsep directly from the FNFT C-library.

    Returns:

        options : NsepOptionsStruct for nsep_wrapper

    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsep_default_opts
    clib_func.restype = NsepOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsep_options(opts=None):
    """Print options of a NsepOptionsStruct.

    When called without additional arguments, the default options from FNFT are printed.

    Optional arguments:

        opts : NsepOptionsStruc, e.g. created by get_nsep_options

    """
    if opts is None:
        opts = fnft_nsep_default_opts_wrapper()
    print(repr(opts))


def get_nsep_options(loc=None, filt=None, bb=None, maxev=None, dis=None, nf=None):
    """Get a NsepOptionsStruct struct for use with nsep_wrapper.

    When called without additional optional argument, the default values from FNFT are used.

    Optional arguments:

        loc : localization of spectrum, default = 2

            0=subsample and refine
            1=gridsearch
            2=mixed

        filt : filtering of spectrum, default = 2

            0=none
            1=manual
            2=auto

        bb : bounding box used for manual filtering, default = [-inf, inf, -inf, inf]

        maxev : maximum number of evaluations for root refinement, default = 20

        nf : normalization flag, default = 1

            0=off
            1=on

        dis : discretization, default = 1

            0=2split2modal
            1=2split2a
            2=2split4a
            3=2split4b
            4=BO

    Returns:

        options : NsepOptionsStruct

    """
    opts = fnft_nsep_default_opts_wrapper()
    if loc is not None:
        opts.localization = loc
    if filt is not None:
        opts.filtering = filt
    if nf is not None:
        opts.normalization_flag = nf
    if dis is not None:
        opts.discretization = dis
    if bb is not None:
        opts.bounding_box[0] = bb[0]
        opts.bounding_box[1] = bb[1]
        opts.bounding_box[2] = bb[2]
        opts.bounding_box[3] = bb[3]
    if maxev is not None:
        opts.max_evals = maxev
    return opts


#
#  Get and view options for nsep (Nonlinear Schroedinger equation, periodic boundaries)
#


def fnft_nsev_default_opts_wrapper():
    """Get the default options for nsev directly from the FNFT C-library.

    Returns:

        options : NsevOptionsStruct with options for nsev_wrapper

    """

    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsev_default_opts
    clib_func.restype = NsevOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsev_options(opts=None):
    """Print options of a NsevOptionsStruct.

    When called without additional argument, the default options from FNFT are printed.


    Optional arguments:

        opts : NsevOptionsStruct, e.g. created by get_nsev_options()

    """

    if opts is None:
        opts = fnft_nsev_default_opts_wrapper()
    print(repr(opts))


def get_nsev_options(bsf=None, bsl=None, niter=None, Dsub=None, dst=None, cst=None, nf=None, dis=None):
    """Get a NsevOptionsStruct for use with nsev_wrapper.

        When called without additional optional arguments, the default values from FNFT are used.

    Optional arguments:

        bsf : bound state filtering, default = 2

            0=none
            1=basic
            2=full

        bsl : bound state localization, default = 2

            0=fast eigenvalue
            1=Newton
            2=subsample and refine

        niter : number of iterations for Newton bound state location, default = 10

        Dsub : number of samples used for 'subsampling and refine'-method, default = 0 (auto)

        dst : type of discrete spectrum, default = 0

            0=norming constants
            1=residues
            2=both

        cst : type of continuous spectrum, default = 0

            0=reflection coefficient
            1=a and b
            2=both

        dis : discretization, default = 3

            0=2split2modal
            1=2split2a
            2=2split4a
            3=2split4b
            4=BO

        nf : normalization flag, default =  1

            0=off
            1=on

    Returns:

        options : NsevOptionsStruct

    """
    opts = fnft_nsev_default_opts_wrapper()
    if bsf is not None:
        opts.bound_state_filtering = bsf
    if bsl is not None:
        opts.bound_state_localization = bsl
    if niter is not None:
        opts.niter = niter
    if Dsub is not None:
        opts.Dsub = Dsub
    if dst is not None:
        opts.discspec_type = dst
    if cst is not None:
        opts.contspec_type = cst
    if nf is not None:
        opts.normalization_flag = nf
    if dis is not None:
        opts.discretization = dis
    return opts


def fnft_nsev_inverse_default_opts_wrapper():
    """Get the default options for nsev_inverse directly from the FNFT C-library.

    Returns:

        options : NsevInverseOptionsStruct with options for nsev_inverse_wrapper

    """

    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsev_inverse_default_opts
    clib_func.restype = NsevInverseOptionsStruct
    clib_func.argtpes = []
    return clib_func()


def print_nsev_inverse_options(opts=None):
    """Print options of a NsevInverseOptionsStruct for nsev_inverse.

    When called without additional argument, the default options from FNFT are printed.


    Optional arguments:

        opts : NsevInverseOptionsStruct, e.g. created by get_nsev_options()
    """

    if opts is None:
        opts = fnft_nsev_inverse_default_opts_wrapper()
    print(repr(opts))


def get_nsev_inverse_options(dis=None, cst=None, csim=None, dst=None, max_iter=None, osf=None):
    """Get a NsevInverseOptionsStruct for use with nsev_inverse_wrapper.

        When called without additional optional arguments, the default values from FNFT are used.

    Optional arguments:

        dis : discretization, default = 3

            0=2split2modal
            1=2split2a
            2=2split4a
            3=2split4b
            4=BO

        cst : type of continuous spectrum, default = 0

            0=Reflection coefficient
            1=b of xi
            2=b of tau

        csim : inversion method for the continuous part, default = 0

            0=default
            1=Transfermatrix with reflection coefficients
            2=Transfermatrix with a,b from iteration
            3=seed potential

        dst : type of discrete spectrum

            0 = norming constants
            1 = residues

        max_iter : maximum number of iterations for iterative methods, default = 100

        osf : oversampling factor

    Returns:

        options : NsevInverseOptionsStruct

    """
    opts = fnft_nsev_inverse_default_opts_wrapper()
    if dis is not None:
        opts.discretization = dis
    if cst is not None:
        opts.contspec_type = cst
    if csim is not None:
        opts.contspec_inversion_method = csim
    if dst is not None:
        opts.discspec_type = dst
    if max_iter is not None:
        opts.max_iter = max_iter
    if osf is not None:
        opts.oversampling_factor = osf
    return opts




