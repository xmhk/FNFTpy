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

Christoph Mahnke, 2018-2021

"""

from FNFTpy import kdvv
import numpy as np


def kdvv_example(dis=None, bsl=None, bsg=None, niter=None, dst=None, cst=None, nf=None,
                 ref=None, K=None, amplitude_scale=1.0, verbose=True):
    """Mimics the C example for calling fnft_kdvv, can be modified with options"""
    if verbose:
        print("\n\nkdvv example")
    # set values
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(D, dtype=np.complex128)
    q[:] = amplitude_scale * 2.0 + 0.0j
    Xi1 = -2
    Xi2 = 2
    M = 8
    if K is None:
        K = D
    Xivec = np.linspace(Xi1, Xi2, M)
    # call function
    res = kdvv(q, tvec, K, M, Xi1=Xi1, Xi2=Xi2,
               dis=dis, bsl=bsl, niter=niter, dst=dst, cst=cst, nf=nf,
               ref=ref, bsg=bsg)
    # print results
    if verbose:
        print("\n----- options used ----")
        print(res['options'])
        print("\n------ results --------")
        print("FNFT return value: %d (should be 0)" % res['return_value'])
        print("continuous spectrum: ")
        for i in range(len(res['cont_ref'])):
            print("%d : Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i],
                                                  np.real(res['cont_ref'][i]), np.imag(res['cont_ref'][i])))
        print("discrete spectrum:")
        print("bound state at %.4f   %.4fi  with norming constant %.4f  %.4f" % (
            np.real(res['bound_states'][0]), np.imag(res['bound_states'][0]), np.real(res['disc_norm'][0]),
            np.imag(res['disc_norm'][0]),
        ))
    return res


def kdvv_example_mex4(log2D, dis=0, diskey="", verbose=True):
    """calculation of bound states, similar to mex example 4

    Exact values of the bound states

    bound_states_exact = [1i,3i];
    normconsts_exact = [-9e6, 729e18];
    """
    T1 = 0;
    T2 = 16
    Xi1 = 0.5;
    Xi2 = 23
    tvec = np.linspace(T1, T2, 2 ** log2D)
    xivec = np.linspace(Xi1, Xi2, 2 ** log2D)
    A = 15.0
    d = 0.5
    exp_t0 = 3000.
    q = A * (1. / np.cosh((tvec - np.log(exp_t0)) / d)) ** 2
    res = kdvv(q, tvec, M=2 ** log2D, Xi1=Xi1, Xi2=Xi2, cst=4, dis=dis, bsl=1, niter=20)
    if verbose:
        print("dis=%d (%s) ... bound states: " % (dis, diskey), res['bound_states'], "  norm const", res['disc_norm'])
    return res
