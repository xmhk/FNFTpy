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
import numpy as np
from FNFTpy import kdvv

class kdvvexample(Testobj):
    """Mimics the C example for calling fnft_kdvv."""
    def example_code(self):
        self.print("\n\nkdvv example")
        # set values
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(D, dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        Xi1 = -2
        Xi2 = 2
        M = 8
        Xivec = np.linspace(Xi1, Xi2, M)
        # call function
        res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2)
        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")
        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("continuous spectrum: ")
        for i in range(len(res['cont'])):
            self.print("%d : Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i],
                  np.real(res['cont'][i]), np.imag(res['cont'][i])))
        self.res =res

    def testconditions(self):
        self.infostr = "Mimic kdvv C example."
        shouldberes = {'cont': np.array([
            0.15329981+0.12203649j,  0.24385425+0.09606438j,
            0.12418466-0.00838456j, -0.46324501+0.20526334j,
            -0.46324501-0.20526334j,  0.12418466+0.00838456j,
            0.24385425-0.09606438j,  0.15329981-0.12203649j])}
        self.single_test(self.test_value, self.res['return_value'], 0, "FNFT return value")
        self.single_test(self.test_array_value, self.res['cont'], shouldberes['cont'], "continuous spectrum")


