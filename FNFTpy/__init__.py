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

Christoph Mahnke, 2018 - 2023

"""

from .auxiliary import get_lib_path, get_fnft_version, print_fnft_version, cmplxrpr

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper, kdvv
from .fnft_manakovv_wrapper import manakovv_wrapper, manakovv
from .fnft_nsep_wrapper import nsep_wrapper, nsep
from .fnft_nsev_wrapper import nsev_wrapper, nsev
from .fnft_nsev_inverse_wrapper import nsev_inverse_xi_wrapper, nsev_inverse_wrapper, nsev_inverse
from .typesdef import *
from .options_handling import *

