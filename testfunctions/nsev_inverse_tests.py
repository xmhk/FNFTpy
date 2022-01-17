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

Christoph Mahnke, 2018-2020

"""

import unittest

from .array_test import *
from examples import nsev_inverse_example, nsev_inverse_example2
from FNFTpy import nsev_inverse_xi_wrapper, nsev_inverse


class NsevInverseExample(unittest.TestCase):
    """Testcase for nsev_inverse_example, (mimic of C example)."""

    def setUp(self):
        self.res = nsev_inverse_example()
        self.expected = {'q': np.array([-8.51156134e-07 - 2.59723802e-03j, -8.51152031e-07 - 5.05389982e-03j,
                                        -8.51152828e-07 - 9.77009846e-03j, -8.51153739e-07 - 1.88124421e-02j,
                                        -8.51154704e-07 - 3.61352219e-02j, -8.51155662e-07 - 6.93026882e-02j,
                                        -8.51156430e-07 - 1.32772848e-01j, -8.51156724e-07 - 2.54100125e-01j,
                                        -8.51156012e-07 - 4.85242920e-01j, -8.51152998e-07 - 9.20351895e-01j,
                                        -8.51144440e-07 - 1.70480071e+00j, -8.51123774e-07 - 2.91920894e+00j,
                                        -8.51093260e-07 - 4.03290079e+00j, -8.51159989e-07 - 2.42570391e-03j,
                                        -8.51157880e-07 - 5.62308393e-04j, -8.51156117e-07 - 4.40370675e-04j,
                                        -8.51154654e-07 - 3.63745902e-04j, -8.51153407e-07 - 3.03868218e-04j,
                                        -8.51152359e-07 - 2.54859627e-04j, -8.51151499e-07 - 2.14146911e-04j,
                                        -8.51150765e-07 - 1.80118348e-04j, -8.51150137e-07 - 1.51591858e-04j,
                                        -8.51149618e-07 - 1.27638782e-04j, -8.51149196e-07 - 1.07506128e-04j,
                                        -8.51148829e-07 - 9.05737153e-05j, -8.51148517e-07 - 7.63264783e-05j]),
                         'Xi': np.array([-401.33884499, 401.73116058])}

    def test_nsev_inverse_example(self):
        with self.subTest('check FNFT nsev_inverse return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev_inverse return value not 0")
        with self.subTest('q value'):
            self.assertTrue(check_array(self.res['q'][0:-1:40],
                                        self.expected['q']), "q values not as expected")
        with self.subTest('Xi value'):
            self.assertTrue(check_array(self.res['Xi'], self.expected['Xi']), "xi values not as expected")


class NsevInverseExample2(unittest.TestCase):
    """Testcase for nsev_inverse_example2."""

    def setUp(self):
        self.res = nsev_inverse_example2()
        self.expected = {'q': np.array([1.34230102e-06 - 5.04465255e-15j, 4.34817385e-06 - 6.31865362e-15j,
                                        1.40574450e-05 - 3.14973971e-15j, 4.54326063e-05 - 2.19330861e-15j,
                                        1.46827533e-04 - 1.55620563e-15j, 4.74508381e-04 - 2.66429125e-16j,
                                        1.53348456e-03 + 2.32701341e-16j, 4.95580127e-03 + 2.84806416e-16j,
                                        1.60155854e-02 + 3.90817711e-16j, 5.17513079e-02 + 1.71484418e-15j,
                                        1.67026494e-01 + 4.65750576e-15j, 5.32522012e-01 + 7.39474890e-15j,
                                        1.50907411e+00 + 3.81190249e-15j, 2.13338526e+00 + 5.18397891e-15j,
                                        1.00280857e+00 + 6.77405341e-15j, 3.26530063e-01 + 4.90563790e-15j,
                                        1.01548385e-01 + 1.62058722e-15j, 3.14376794e-02 + 1.95891048e-16j,
                                        9.72830255e-03 + 2.30171230e-16j, 3.01026309e-03 + 5.24089935e-16j,
                                        9.31471124e-04 + 4.39924210e-16j, 2.88226276e-04 - 6.56173293e-16j,
                                        8.91859214e-05 - 1.96145018e-15j, 2.75963271e-05 - 2.67063774e-15j,
                                        8.53801078e-06 - 4.81025786e-15j, 2.63963808e-06 - 7.13301617e-15j])}

    def test_return_value(self):
        with self.subTest('check FNFT nsev_inverse return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev_inverse return value not 0")
        with self.subTest('q value'):
            self.assertTrue(check_array(self.res['q'][0:-1:40], self.expected['q']), "q values not as expected")


class NsevInverseInputVariation(unittest.TestCase):
    """Testcase for various input examples (discrete spec / contspec / None) for nsev_inverse"""

    def setUp(self):
        D = 512
        M = 2 * D
        Tmax = 15
        tvec = np.linspace(-Tmax, Tmax, D)
        rv, xi = nsev_inverse_xi_wrapper(D, tvec[0], tvec[-1], M)
        xivec = xi[0] + np.arange(M) * (xi[1] - xi[0]) / (M - 1)
        # semi-analytic nonlinear spectrum
        bound_states = np.array([0.7j, 1.7j])
        disc_norming_const_ana = [1.0, -1.0]
        cont_b_ana = 0.587783 / np.cosh(xivec * np.pi) * np.exp(1.0j * np.pi)
        self.xivec = xivec
        self.tvec = tvec
        self.cont_b_ana = cont_b_ana
        self.bound_states = bound_states
        self.disc_norming_const_ana = disc_norming_const_ana
        self.expected = {
            'qsamprange': [0, -1, 40],
            'q_both': np.array(
                [1.34282821e-06 + 5.90905693e-16j, 1.40927340e-05 + 6.69759843e-16j,
                 1.47533087e-04 - 8.49415093e-16j, 1.54437857e-03 + 1.22641929e-16j,
                 1.61660017e-02 + 2.70942564e-15j, 1.68966183e-01 + 9.95269660e-15j,
                 1.52429449e+00 + 1.04462643e-14j, 9.88595941e-01 + 1.57705840e-14j,
                 9.97145517e-02 + 6.45254951e-15j, 9.53104365e-03 + 1.87953249e-15j,
                 9.10510486e-04 - 5.58634639e-16j, 8.69798167e-05 - 7.22303874e-16j,
                 8.30772437e-06 + 9.63333629e-16j]),
            'q_disc': np.array(
                [5.09548061e-09 - 0.j, 1.36459139e-07 - 0.j, 3.65443384e-06 - 0.j,
                 9.78673225e-05 - 0.j, 2.62101136e-03 - 0.j, 7.03972926e-02 - 0.j,
                 1.69330859e+00 - 0.j, 9.18642908e-01 + 0.j, 3.35346003e-02 + 0.j,
                 1.25083775e-03 + 0.j, 4.67066469e-05 + 0.j, 1.74405899e-06 + 0.j,
                 6.51243941e-08 + 0.j]),
            'q_cont': np.array(
                [1.15243924e-07 - 6.57512209e-16j, 1.27802639e-06 + 7.04459178e-16j,
                 1.34080356e-05 + 2.15209454e-16j, 1.40365068e-04 - 1.10360319e-15j,
                 1.46934384e-03 + 4.21307084e-16j, 1.53587945e-02 + 2.81885851e-15j,
                 1.38560954e-01 + 1.43110043e-14j, 8.98666443e-02 + 8.74350146e-15j,
                 9.06369089e-03 + 2.14242869e-15j, 8.66276590e-04 - 1.04369988e-16j,
                 8.27537156e-05 - 9.43644219e-16j, 7.90416963e-06 + 6.57722413e-16j,
                 7.51076324e-07 + 6.32640626e-16j]),
            'q_none': np.array(
                [[0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j,
                  0. + 0.j, 0. + 0.j, 0. + 0.j]])}

    def test_input_both(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, self.bound_states, self.disc_norming_const_ana,
                           cst=1, dst=0)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 0, "nsev_inverse input variation both return value not 0")
        with self.subTest('both : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_both']), "both: q values not as expected")

    def test_input_disc(self):
        res = nsev_inverse(self.xivec, self.tvec, None, self.bound_states, self.disc_norming_const_ana,
                           cst=1, dst=0)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 0,
                             "nsev_inverse input variation disc return value not 0")
        with self.subTest('disc : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_disc']), "disc: q values not as expected")

    def test_input_cont1(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, None, None,
                           cst=1, dst=0)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 0,
                             "nsev_inverse input variation cont1 return value not 0")
        with self.subTest('cont1 : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']),
                            "cont1: q values not as expected")

    def test_input_cont2(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, None, self.disc_norming_const_ana,
                           cst=1, dst=0)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 0,
                             "nsev_inverse input variation cont2 return value not 0")
        with self.subTest('cont2 : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']),
                            "cont2: q values not as expected")

    def test_input_cont3(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, self.bound_states, None,
                           cst=1, dst=0)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 0,
                             "nsev_inverse input variation cont3 return value not 0")
        with self.subTest('cont3 : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']),
                            "cont3: q values not as expected")

    def test_return_value_none(self):
        res = nsev_inverse(self.xivec, self.tvec, None, None, None,
                           cst=1, dst=0, display_c_msg=False)
        with self.subTest('FNFT nsev_inverse return value'):
            self.assertEqual(res['return_value'], 7,
                             "nsev_inverse input variation none return value not 7")
        with self.subTest('none : q value'):
            self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_none']),
                            "none: q values not as expected")

    def test_q_value_cont1(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, None, None,
                           cst=1, dst=0)
        self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']), "cont1: q values not as expected")

    def test_q_value_cont2(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, None, self.disc_norming_const_ana,
                           cst=1, dst=0)
        self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']), "cont2: q values not as expected")

    def test_q_value_cont3(self):
        res = nsev_inverse(self.xivec, self.tvec, self.cont_b_ana, self.bound_states, None,
                           cst=1, dst=0)
        self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_cont']), "cont3: q values not as expected")

    def test_q_value_none(self):
        res = nsev_inverse(self.xivec, self.tvec, None, None, None,
                           cst=1, dst=0, display_c_msg=False)
        self.assertTrue(check_array(res['q'][0:-1:40], self.expected['q_none']), "none: q values not as expected")
