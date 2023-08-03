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

Christoph Mahnke, 2018-2023

"""

from FNFTpy import nsev_inverse, nsev_inverse_xi_wrapper, cmplxrpr
import numpy as np


def nsev_inverse_example(verbose=True):
    """Mimics the C example for calling fnft_nsev_inverse."""
    if verbose:
        print("\nnsev inverse example")

    # set values
    M = 2048
    D = 1024
    tvec = np.linspace(-2, 2, D)
    T1 = tvec[0]
    T2 = tvec[-1]
    alpha = 2.0
    beta = 0.55
    gamma = np.sqrt(np.abs(alpha) ** 2 + np.abs(beta) ** 2)
    kappa = 1

    # get the frequency intervall suited for the given time vector
    rv, XI = nsev_inverse_xi_wrapper(D, T1, T2, M)
    Xi1 = XI[0]
    Xi2 = XI[1]
    xivec = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)

    # set continuous spectrum
    contspec = alpha / (xivec - beta * 1.0j)

    # set discrete spectrum
    bound_states = np.array([1.0j * beta])
    normconst_or_residues = np.array([-1.0j * alpha / (gamma + beta)])

    # call function
    res = nsev_inverse(xivec, tvec, contspec, bound_states, normconst_or_residues)

    # print results
    if verbose:
        print("\n----- options used ----")
        print(res['options'])
        print("\n------ results --------")
        print("FNFT return value: %d (should be 0)" % res['return_value'])
        print("Total number of samples calculated: %d" % D)
        print("some samples:")
        for i in range(0, D, 64):
            print("  %d : q(t=%.5f) = %s " % (i, tvec[i], cmplxrpr((res['q'][i]))))
    res['Xi'] = np.array([Xi1, Xi2])
    return res


def nsev_inverse_example2():
    """nsev_inverse_example: create a N=2.2 Satsuma-Yajima pulse from nonlinear spectrum."""
    D = 1024
    M = 2 * D
    Tmax = 15
    tvec = np.linspace(-Tmax, Tmax, D)
    # calculate suitable frequency bonds (xi)
    rv, xi = nsev_inverse_xi_wrapper(D, tvec[0], tvec[-1], M)
    xivec = xi[0] + np.arange(M) * (xi[1] - xi[0]) / (M - 1)

    # analytic field: chirp-free N=2.2 Satsuma-Yajima pulse
    q = 2.2 / np.cosh(tvec)

    # semi-analytic nonlinear spectrum
    bound_states = np.array([0.7j, 1.7j])
    disc_norming_const_ana = [1.0, -1.0]
    cont_b_ana = 0.587783 / np.cosh(xivec * np.pi) * np.exp(1.0j * np.pi)

    # call the function
    res = nsev_inverse(xivec, tvec, cont_b_ana, bound_states, disc_norming_const_ana, cst=1, dst=0)
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")

    print("FNFT return value: %d (should be 0)" % res['return_value'])
    # compare result to analytic function
    print("nsev-inverse example: Satsuma-Yajima N=2.2")
    print("Difference analytic - numeric: sum((q_ana-q_num)**2) = %.2e  (should be approx 0) " % np.sum(
        np.abs(q - res['q']) ** 2))
    return res
