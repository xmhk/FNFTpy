"""
This file is part of FNFTpy.
FNFTpy provides wrapper functions to interact with FNFT,
a library for the numerical computation of nonlinear Fourier transforms.

For FNFTpy to work, a copy of FNFT has to be installed.
For general information, source files and installation of FNFT,
visit FNFT's github page: https://github.com/FastNFT

For information about setup and usage of FNFTpy see README.md.

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


def get_lib_path():
    """Return the path of the FNFT file.

    Here you can set the location of the compiled library for FNFT.
    See example strings below.

    Returns:

        libstring : string holding library path

    Example paths:

        libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
        libstr = "C:\\Libraries\\local\\libfnft.dll" # windows - with backslash
        libstr = "/usr/local/lib/libfnft.so"  # example for linux

    """
    libstr = "/usr/local/lib/libfnft-devel.so"  # example for linux
    return libstr


def check_value(val, vmin, vmax, vtype=int):
    """Raise and ValueError when variable has wrong type or is out of range.

        Arguments:

            val : variable to check
            vmin : minimum value val should take
            vmax : maximum value val should take

        Optional arguments:

            vtype : type val should take
    """
    if type(val) != vtype:
        raise ValueError("Type mismatch expected {}, got {}".format(vtype, type(val)))
    if not (vmin <= val <= vmax):
        raise ValueError("Value Error: variable out of range")
