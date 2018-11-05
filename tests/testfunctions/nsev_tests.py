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
from FNFTpy import nsev
import numpy as np

class nsevexample(Testobj):
    def example_code(self):
        """Mimics the C example for calling fnft_nsev."""
        self.print("\n\nnsev example")

        # set values
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(len(tvec), dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        M = 8
        Xi1 = -2
        Xi2 = 2
        Xivec = np.linspace(Xi1, Xi2, M)

        # call function
        res = nsev(q, tvec, M=M, Xi1=Xi1, Xi2=Xi2)

        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")

        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("continuous spectrum")
        for i in range(len(res['cont_ref'])):
            self.print("%d :  Xi = %.4f   %.6f  %.6fj" % (
            i, Xivec[i], np.real(res['cont_ref'][i]), np.imag(res['cont_ref'][i])))
        self.print("discrete spectrum")
        for i in range(len(res['bound_states'])):
            self.print("%d : %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                       np.imag(res['bound_states'][i]),
                                                                       np.real(res['disc_norm'][i]),
                                                                       np.imag(res['disc_norm'][i])))
        self.res = res

    def testconditions(self):
        self.infostr="Mimic nsev C example."
        shouldberes = {'bound_states_num': 1,
                       'bound_states': np.array([2.13821177e-50+1.57422601j]),
                       'disc_norm': np.array([-1.-2.56747175e-50j]),
                       'cont_ref': np.array([
                           -0.10538565-0.42577137j, -0.78378026-1.04297186j,
                            -1.09090439-1.33957378j, -1.16918546-0.48325228j,
                            -1.16918546+0.48325228j, -1.09090439+1.33957378j,
                            -0.78378026+1.04297186j, -0.10538565+0.42577137j]),
                       }
        self.single_test(self.test_value, self.res['return_value'], 0, "FNFT return value")
        self.single_test(self.test_value, self.res['bound_states_num'], 1, "number of bound states")
        self.single_test(self.test_array_value, self.res['bound_states'], shouldberes['bound_states'], "bound states")
        self.single_test(self.test_array_value, self.res['disc_norm'], shouldberes['disc_norm'], 'norming consts')
        self.single_test(self.test_array_value, self.res['cont_ref'], shouldberes['cont_ref'],'cont. reflection coeff.')




