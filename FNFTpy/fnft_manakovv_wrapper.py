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

#def nsev(q, tvec, Xi1=-2, Xi2=2, M=128, K=128, kappa=1, bsf=None,
#         bsl=None, niter=None, Dsub=None, dst=None, cst=None, nf=None, dis=None, ref=None,
#         bound_state_guesses = None):

#def nsev_wrapper(D, q, T1, T2, Xi1, Xi2,
#                 M, K, kappa, options, bound_state_guesses = None):

#FNFT_INT fnft_manakovv(
# const FNFT_UINT D,
# FNFT_COMPLEX const* const q1,
# FNFT_COMPLEX const* const q2,
#	FNFT_REAL const* const T,
#	const FNFT_UINT M,
#	FNFT_COMPLEX* const contspec,
#	FNFT_REAL const* const XI,
#	FNFT_UINT* const K_ptr,
#	FNFT_COMPLEX* const bound_states,
#	FNFT_COMPLEX* const normconsts_or_residues,
#	const FNFT_INT kappa,
#	fnft_manakovv_opts_t* opts);

def manakovv_wrapper(D, q1, q2, T1, T2, Xi1, Xi2, M, K, kappa  ):
    a= 1
    pass
