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

import unittest

from .array_test import *
from examples import nsev_example
from FNFTpy import nsev


class NsevExampleTest(unittest.TestCase):
    """Testcase for nsev_example, (mimic of C example)."""

    def setUp(self):
        self.res = nsev_example()
        self.expected = {'bound_states': np.array([2.13821177e-50 + 1.57422601j]),
                         'disc_norm': np.array([-1. - 2.56747175e-50j]),
                         'cont_ref': np.array([
                             -0.10538565 - 0.42577137j, -0.78378026 - 1.04297186j,
                             -1.09090439 - 1.33957378j, -1.16918546 - 0.48325228j,
                             -1.16918546 + 0.48325228j, -1.09090439 + 1.33957378j,
                             -0.78378026 + 1.04297186j, -0.10538565 + 0.42577137j])}

    def test_nsev_example(self):
        with self.subTest('check FNFT nsev return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev return value not 0")
        with self.subTest('bound states number'):
            self.assertEqual(self.res['bound_states_num'], 1, "bound_states_num not 1")
        with self.subTest('bound states value'):
            self.assertTrue(check_array(self.res['bound_states'], self.expected['bound_states']),
                            "bound_states value not as expected")
        with self.subTest('disc_norm value'):
            self.assertTrue(check_array(self.res['disc_norm'], self.expected['disc_norm']),
                            "disc_norm value not as expected")
        with self.subTest('cont_ref value'):
            self.assertTrue(check_array(self.res['cont_ref'], self.expected['cont_ref']),
                            "cont_ref value not as expected")


class NsevDstCstInputTest(unittest.TestCase):
    """Testcase for various input for nsev."""

    def setUp(self):
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(len(tvec), dtype=np.complex128)
        q[:] = 2.3 / np.cosh(tvec)
        res = {}
        # different switches for discrete spectrum type
        for dst in [-1, 0, 1, 2, 3]:
            tmpres = nsev(q, tvec, dst=dst, )
            res['dst=%d' % dst] = np.array([tmpres['return_value'] == 0,
                                            'disc_res' in tmpres.keys(),
                                            'disc_norm' in tmpres.keys()])
        # different switches for continuous spectrum type
        for cst in [-1, 0, 1, 2, 3]:
            tmpres = nsev(q, tvec, cst=cst, )
            res['cst=%d' % cst] = np.array([
                tmpres['return_value'] == 0,
                'cont_ref' in tmpres.keys(),
                'cont_a' in tmpres.keys(),
                'cont_b' in tmpres.keys()])
        # calulate neither discrete nor continuous spectrum
        tmpres = nsev(q, tvec, dst=3, cst=3)
        res['dst=3cst=3'] = np.array([tmpres['return_value'] == 0,
                                      'disc_res' in tmpres.keys(),
                                      'disc_norm' in tmpres.keys(),
                                      'cont_ref' in tmpres.keys(),
                                      'cont_a' in tmpres.keys(),
                                      'cont_b' in tmpres.keys()
                                      ])
        self.res = res

    def test_dst_cst_variation(self):
        expected = {'dst=-1': np.array([True, False, False]),
                    'dst=0': np.array([True, False, True]),
                    'dst=1': np.array([True, True, False]),
                    'dst=2': np.array([True, True, True]),
                    'dst=3': np.array([True, False, False]),
                    'cst=-1': np.array([True, False, False, False]),
                    'cst=0': np.array([True, True, False, False]),
                    'cst=1': np.array([True, False, True, True]),
                    'cst=2': np.array([True, True, True, True]),
                    'cst=3': np.array([True, False, False, False]),
                    'dst=3cst=3': np.array([True, False, False, False, False, False])}
        for k in expected.keys():
            with self.subTest(key=k):
                self.assertTrue(check_boolarray(self.res[k], expected[k]), "unexpected output")
