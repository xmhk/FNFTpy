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
from warnings import warn
from .typesdef import *


def get_lib_path():
    """Return the path of the FNFT file.

    Edit this function to set the location of the compiled library for FNFT.
    See example strings below.

    Returns:

    * libstring : string holding library path

    Example paths:

        * libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
        * libstr = "/usr/local/lib/libfnft.so"  # example for linux

    """
    #libstr = "/usr/local/lib/libfnft.so.0.2.2-dev"
    libstr = "/usr/local/lib/libfnft.so.0.4.0"

    return libstr


def get_fnft_version():
    """
    Get the version of FNFT used by calling fnft_version.

    Returns:

    * rdict: dictionary holding the fields:
        * return_value : return value from FNFT
        * major : major version number
        * minor : minor version number
        * patch : patch level
        * suffix : suffix string

    """
    suffix_maxlen = 8  # defined in  FNFT/include/fnft_config.h.in
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_versionf = fnft_clib.fnft_version
    clib_versionf.restype = ctypes_int
    version_major = ctypes_uint(0)
    version_minor = ctypes_uint(0)
    version_patch = ctypes_uint(0)
    suffix_buff = ctypes.create_string_buffer(suffix_maxlen)
    clib_versionf.argtypes = [
        ctypes.POINTER(ctypes_uint),
        ctypes.POINTER(ctypes_uint),
        ctypes.POINTER(ctypes_uint),
        type(suffix_buff)]

    rv = clib_versionf(ctypes.byref(version_major),
                       ctypes.byref(version_minor),
                       ctypes.byref(version_patch),
                       suffix_buff)
    check_return_code(rv)

    rdict = {
        'return value': rv,
        'major': int(version_major.value),
        'minor': int(version_minor.value),
        'patch': int(version_patch.value),
        'suffix': suffix_buff.value.decode('UTF-8')}
    return rdict


def print_fnft_version():
    """
    Prints the  path and the version of FNFT library used.
    """
    pathloc = get_lib_path()
    versiondict = get_fnft_version()
    print("\n FNFT library location: %s" % pathloc)
    print("               version: %d.%d.%d%s" % (versiondict['major'],
                                                  versiondict['minor'],
                                                  versiondict['patch'],
                                                  versiondict['suffix']))


def check_value(val, vmin, vmax, vtype=int):
    """Raise and ValueError when variable has wrong type or is out of range.

    Arguments:

    * val : variable to check
    * vmin : minimum value val should take
    * vmax : maximum value val should take

    Optional arguments:

    * vtype : type val should take
    """
    if type(val) != vtype:
        raise ValueError("Type mismatch expected {}, got {}".format(vtype, type(val)))
    if not (vmin <= val <= vmax):
        raise ValueError("Value Error: variable out of range")


def check_return_code(rv):
    """Check the return code of a library call. Give warning if Code is not 0.

    Arguments:

    * rv : return value

    """
    if rv == 0:
        pass
    else:
        wstring = "An error occured when calling FNFT: error code %d" % rv
        warn(wstring)
