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

from .testobj_class import Testobj
from FNFTpy import nsep
import numpy as np


class nsepexample(Testobj):
    """Mimics the C example for calling fnft_nsep."""
    def run_test(self):
        self.print("\n\nnsep example")
        # set values
        D = 256
        dt = 2 * np.pi / D
        tvec = np.arange(D) * dt
        q = np.exp(2.0j * tvec)
        # call function
        res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")
        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("number of samples: %d" % D)
        self.print('main spectrum')
        for i in range(res['K']):
            self.print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                         np.imag(res['main'][i])))
        self.print('auxiliary spectrum')
        for i in range(res['M']):
            self.print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                         np.imag(res['aux'][i])))
        self.res = res

    def testconditions(self):
        print(self.test_value(self.res['return_value'],0))
        print(self.key_is_in_list('return_value', self.res.keys()))