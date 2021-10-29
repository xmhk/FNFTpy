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

Christoph Mahnke, 2021

"""

from FNFTpy import manakovv, print_manakovv_options
import numpy as np


def manakovv_example(D=1024, M=8, K=None, T1=-2, T2=2, Xi1=-1.75, Xi2=2, kappa=1, bsf=None,
                     bsl=None, niter=None, Dsub=None, dst=None, cst=None,
                     nf=None, dis=None, ref=None, verbose=True):
    """ mimics the manakovv C example from FNFT """
    def cplxprint(z):
        s = "%.4e\t%.4ej" % (np.real(z), np.imag(z))
        return s

    q1 = np.zeros(D, dtype=np.complex128)
    q2 = np.zeros(D, dtype=np.complex128)
    tvec = np.linspace(T1, T2, D)
    # standard
    q1[:] = 2.0 + 0.0j
    q2[:] = .650 + 0.0j
    if K is None:
        K = D
    Xivec = np.linspace(Xi1, Xi2, M)
    res = manakovv(q1, q2, tvec, M=M, K=K, Xi1=Xi1, Xi2=Xi2,
                   dis=dis, bsf=bsf, bsl=bsl, niter=niter, Dsub=Dsub,
                   dst=dst, cst=cst,
                   nf=nf, ref=ref)
    if verbose:
        print("-- options used --")
        print_manakovv_options(res['options'])
        print("-- continuous spectrum ---\n")
        print("                  \t part 1\t\t\t\t\t\t part2")
        for i in range(M):
            print("%d Xi = %.5f  \t%s \t%s" % (i + 1, Xivec[i],
                                               cplxprint(res['cont_ref1'][i]),
                                               cplxprint(res['cont_ref2'][i])))
    return res


def mex_fnft_manakov_example(M=8):
    """resembles the calculation done in mex_fnft_manakovv_example"""
    D = 512
    tvec = np.linspace(-5, 5, D)
    Xi1 = -7.0 / 4.
    Xi2 = 8.0 / 4.
    q1 = 0.8 / np.cosh(tvec)
    q2 = 5.2 / np.cosh(tvec)
    res = manakovv(q1, q2, tvec, Xi1, Xi2, M=M)
    return res
