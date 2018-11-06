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
    def example_code(self):
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
        self.infostr = "Mimic nsep C example."
        expected = {
                      'K': 11,
                      'main': np.array([-0.99999999-8.65909473e-01j, -0.99999999-8.65909475e-01j,
                                     -0.99999999+8.65909475e-01j, -0.99999999+8.65909474e-01j,
                                     -0.99999999-9.99899604e-01j, -0.99999999+9.99899604e-01j,
                                      0.1180403 +6.56652320e-08j,  1.2914677 +1.11864992e-08j,
                                     -0.99977766-6.49652790e-06j,  0.73224594-1.84219275e-09j,
                                     1.8286518 +1.74944489e-08j]),
                      'M': 7,
                      'aux': np.array([-0.99999999-8.65909474e-01j, -0.99999999+8.65909474e-01j,
                                    -0.99993896+1.87820258e-08j,  0.11814625+2.82216353e-07j,
                                     0.73222476+1.12819764e-08j,  1.29151798+6.35545312e-08j,
                                    1.82871124+8.88012865e-08j])}
        self.single_test(self.test_value, self.res['return_value'], 0, "FNFT return value")
        self.single_test(self.test_value, self.res['K'], 11, "K")
        self.single_test(self.test_value, self.res['M'], 7,"M")
        # as the order of spectra is not clear, we round to 8 digits, sort and compare
        # to sample data
        self.single_test(self.test_array_value,
                         np.sort_complex(np.around(self.res['main'],8)),
                         np.sort_complex(expected['main']), "main spectrum")
        self.single_test(self.test_array_value,
                         np.sort_complex(np.around(self.res['aux'],8)),
                         np.sort_complex(expected['aux']), "auxiliary spectrum")
