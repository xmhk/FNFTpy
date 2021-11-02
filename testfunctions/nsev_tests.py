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
import numpy as np
from .array_test import relnorm, check_boolarray
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
            self.assertTrue(relnorm(self.expected['bound_states'], self.res['bound_states']) < 1e-8,
                            "bound_states value not as expected")
        with self.subTest('disc_norm value'):
            self.assertTrue(relnorm(self.expected['disc_norm'], self.res['disc_norm']) < 1e-13,
                            "disc_norm value not as expected")
        with self.subTest('cont_ref value'):
            self.assertTrue(relnorm(self.expected['cont_ref'], self.res['cont_ref']) < 1e-8,
                            "cont_ref value not as expected")


class NsevExampleTestBoundStateGuesses(unittest.TestCase):
    """Testcase for nsev_example, check whether works with provided bound_states."""

    def setUp(self):
        self.res = nsev_example(verbose=False, dst=2, cst=4, bsl=1,
                                bsg=[0.01 + 0.1j, 1j],
                                amplitude_scale=1.2)
        self.expected = {'bound_states': np.array([-1.97215226e-29 + 0.21057155j, 0.00000000e+00 + 2.02789446j]),
                         'disc_norm': np.array([1. + 7.8106363e-30j, -1. - 0.0000000e+00j]),
                         }

    def test_nsev_example(self):
        with self.subTest('check FNFT nsev return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev return value not 0")
        with self.subTest('bound states value'):
            self.assertTrue(relnorm(self.expected['bound_states'], self.res['bound_states']) < 1e-8,
                            "provide guesses: bound_states value not as expected")
        with self.subTest('disc_norm value'):
            self.assertTrue(relnorm(self.expected['disc_norm'], self.res['disc_norm']) < 1e-14,
                            "provide guesses: disc_norm value not as expected")


class NsevExampleTestBoundStateGuessesMex4(unittest.TestCase):
    """Testcase for nsev_example, check whether works with provided bound_states.

    based on mex_fnft_nsev_example_4.m"""

    def setUp(self):
        D = 2 ** 10
        tvec = np.linspace(-32, 32, D)
        qo = 5.4
        lam0 = 3.0
        q = np.multiply(qo / np.cosh(tvec), np.exp(-2.0j * tvec * lam0))
        self.bs_exact = lam0 + 1.0j * (qo + 0.5 - np.floor(np.arange(qo + 0.5, 1, -1)))

        # stochastic may not be good to have some reliable test function
        # bsguesses = bs_exact+0.035*np.exp(1j*np.pi*np.random.rand(5))
        bsguesses = self.bs_exact + np.array(
            [0.00045826 + 0.034997j,
             -0.01167859 + 0.0329941j,
             0.01942237 + 0.02911651j,
             0.03171094 + 0.0148127j,
             -0.0339977 + 0.00831603j])
        self.norm_exact = (-1) ** (np.arange(np.floor(qo + 0.5), 0, -1))
        self.res = nsev(q, tvec, cst=3, dis=22, bsl=1, niter=20, bsg=bsguesses)

    def test_nsev_example_mex4(self):
        with self.subTest('check FNFT nsev return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev return value not 0")
        with self.subTest('bound states value'):
            self.assertTrue(relnorm(self.bs_exact, self.res['bound_states']) < 5e-5,
                            "provide guesses (mex4): bound_states value not as expected")

        with self.subTest('disc_norm value'):
            self.assertTrue(relnorm(self.norm_exact, self.res['disc_norm']) < 1e-14,
                            "provide guesses: disc_norm value not as expected")


class NsevExampleTestRF(unittest.TestCase):
    """Testcase for nsev_example, check whether RF flag works as expected.

    this based on the mex_fnft_nsev_example_2.m file of FNFT.

    It should show that the Richardson Extrapolation improves accuracy"""

    def setUp(self):
        D = 2 ** 11
        tvec = np.linspace(-32, 32, D)
        Xi1 = -10;
        Xi2 = 10
        xivec = np.linspace(Xi1, Xi2, D)
        qo = 5.4 + 0.0j
        lam0 = 3.0
        q = np.multiply(qo / np.cosh(tvec), np.exp(-2.0j * tvec * lam0))
        self.bexact = -1.0 * np.sin(np.pi * qo) / np.cosh(np.pi * (xivec - lam0))
        self.res1 = nsev(q, tvec, Xi1=Xi1, Xi2=Xi2, M=D, dst=4, cst=1, dis=21, ref=1)
        self.res2 = nsev(q, tvec, Xi1=Xi1, Xi2=Xi2, M=D, dst=4, cst=1, dis=21, ref=0)

    def test_nsev_rf_improvement(self):
        with self.subTest('check FNFT nsev return value'):
            self.assertEqual(self.res1['return_value'], 0, "FNFT nsev return value not 0")
        with self.subTest('check FNFT nsev return value'):
            self.assertEqual(self.res2['return_value'], 0, "FNFT nsev return value not 0")
        with self.subTest('with RF flag accuracy is sufficient'):
            self.assertTrue(relnorm(self.bexact, self.res1['cont_b']) < 2e-7,
                            "with RF flag: accuracy is not sufficient")
        with self.subTest('with RF flag accuracy is sufficient'):
            self.assertTrue(not relnorm(self.bexact, self.res2['cont_b']) < 2e-7,
                            "without RF flag: accuracy is sufficient. unexpected. (check error margin)")
        with self.subTest('check improvement'):
            self.assertTrue(
                relnorm(self.bexact, self.res1['cont_b']) < relnorm(self.bexact, self.res2['cont_b']),
                "RF flag does not improve as expected")


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
