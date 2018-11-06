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

    def run_tests(self):
        self.infostr="Mimic nsev C example."
        expected = {'bound_states_num': 1,
                       'bound_states': np.array([2.13821177e-50+1.57422601j]),
                       'disc_norm': np.array([-1.-2.56747175e-50j]),
                       'cont_ref': np.array([
                           -0.10538565-0.42577137j, -0.78378026-1.04297186j,
                            -1.09090439-1.33957378j, -1.16918546-0.48325228j,
                            -1.16918546+0.48325228j, -1.09090439+1.33957378j,
                            -0.78378026+1.04297186j, -0.10538565+0.42577137j]),
                       }
        self.single_test(self.check_value, self.res['return_value'], 0, "FNFT return value")
        self.single_test(self.check_value, self.res['bound_states_num'], 1, "number of bound states")
        self.single_test(self.check_array, self.res['bound_states'], expected['bound_states'], "bound states")
        self.single_test(self.check_array, self.res['disc_norm'], expected['disc_norm'], "norming consts")
        self.single_test(self.check_array, self.res['cont_ref'], expected['cont_ref'], "cont. reflection coeff.")



class nsev_test_options(Testobj):
    """Check whether the switches dst and cst work for nsev."""
    def example_code(self):
        # set values
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(len(tvec), dtype=np.complex128)
        q[:] = 2.3 / np.cosh(tvec)
        M = 8
        Xi1 = -2
        Xi2 = 2
        self.res={}
        # different switches for discrete spectrum type
        for dst in [-1, 0, 1, 2, 3]:
            tmpres = nsev(q, tvec, dst=dst, )
            self.res['dst=%d'%dst] = np.array([tmpres['return_value']==0,
                    'disc_res' in tmpres.keys(),
                    'disc_norm' in tmpres.keys()])
        # different switches for continuous spectrum type
        for cst in [-1, 0, 1, 2, 3]:
            tmpres = nsev(q, tvec, cst=cst, )
            self.res['cst=%d'%cst] = np.array([
                tmpres['return_value'] == 0,
               'cont_ref' in tmpres.keys(),
               'cont_a' in tmpres.keys(),
               'cont_b' in tmpres.keys()])
        # calulate neither discrete nor continuous spectrum
        tmpres = nsev(q, tvec, dst=3, cst=3)
        self.res['dst=3cst=3'] = np.array([tmpres['return_value']==0,
                                           'disc_res' in tmpres.keys(),
                                           'disc_norm' in tmpres.keys(),
                                           'cont_ref' in tmpres.keys(),
                                           'cont_a' in tmpres.keys(),
                                           'cont_b' in tmpres.keys()
                                           ])

    def run_tests(self):
        self.infostr="checks for dst and cst switches"
        expected = {'dst=-1': np.array([ True, False, False]),
                    'dst=0': np.array([ True, False,  True]),
                    'dst=1': np.array([ True,  True, False]),
                    'dst=2': np.array([ True,  True,  True]),
                    'dst=3': np.array([ True, False, False]),
                    'cst=-1': np.array([ True, False, False, False]),
                    'cst=0': np.array([ True,  True, False, False]),
                    'cst=1': np.array([ True, False,  True,  True]),
                    'cst=2': np.array([ True,  True,  True,  True]),
                    'cst=3': np.array([ True, False, False, False]),
                    'dst=3cst=3': np.array([ True, False, False, False, False, False])}
        for k in expected.keys():
            self.single_test(self.check_boolarray, self.res[k], expected[k], "check option: %s"%k)



