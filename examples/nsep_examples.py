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

from FNFTpy import nsep
import numpy as np


def nsep_example(D=256, loc=None, dis=None, maxev=None, verbose=True):
    """Mimics the C example for calling fnft_nsep."""
    if verbose:
        print("\n\nnsep example")
    # tvec = np.linspace(0, 2*np.pi, D)
    dt = 2 * np.pi / D
    tvec = np.arange(0, D) * dt
    q = np.exp(2.0j * tvec)
    # call function
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1, kappa=1, dis=dis, loc=loc, maxev=maxev)
    # print results
    if verbose:
        print("\n----- options used ----")
        print(res['options'])
        print("\n------ results --------")
        print("FNFT return value: %d (should be 0)" % res['return_value'])
        print("number of samples: %d" % D)
        print('main spectrum')
        for i in range(res['K']):
            print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                         np.imag(res['main'][i])))
        print('auxiliary spectrum')
        for i in range(res['M']):
            print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                         np.imag(res['aux'][i])))
    return res
