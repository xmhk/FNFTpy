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

Christoph Mahnke, 2021

"""

import unittest

from .array_test import *
from examples import manakovv_example, mex_fnft_manakov_example


class ManakovvExampleTest(unittest.TestCase):
    """Testcase for manakovv_example, (mimic of C example)."""

    def setUp(self):
        self.res = manakovv_example(D=256, dis=0, cst=2, verbose=False)

    def test_manakovv_example(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {
            'bound_states_num': 14,
            'cont_ref1': np.array([-0.78609698 + 0.82940082j, 0.00112661 + 0.27523454j,
                                   -0.53227908 + 0.12468494j, 1.05810621 + 0.83874311j,
                                   -0.20693247 - 0.9881531j, -0.13346301 + 0.10490432j,
                                   -0.41497804 - 0.63821938j, -0.52302048 - 0.41081412j]),
            'cont_ref2': np.array([-0.25548152 + 0.26955527j, 0.00036615 + 0.08945123j,
                                   - 0.1729907 + 0.0405226j, 0.34388452 + 0.27259151j,
                                   - 0.06725305 - 0.32114976j, - 0.04337548 + 0.0340939j,
                                   - 0.13486786 - 0.2074213j, - 0.16998165 - 0.13351459j]),
            'cont_a': np.array([
                -0.44004946 - 0.46429227j, 0.0039329 - 0.96057846j, 0.84411964 + 0.19773317j,
                - 0.45127031 + 0.35771436j, 0.14054257 - 0.67112596j, 0.77397222 + 0.60835518j,
                - 0.42556816 + 0.65450852j, - 0.64447174 + 0.50621231j]),
            'cont_b1': np.array([0.73100594 + 1.36898750e-06j, 0.2643888 + 2.70668698e-07j,
                                 - 0.47396158 - 2.24526292e-07j, - 0.77752238 - 7.05553733e-08j,
                                 - 0.69225802 + 1.77957028e-07j, - 0.16711575 + 1.17246741e-07j,
                                 0.59432147 - 8.17024407e-07j, 0.54503108 - 1.31264223e-06j]),
            'cont_b2': np.array([0.23757693 + 4.44920936e-07j, 0.08592636 + 8.79673273e-08j,
                                 - 0.15403751 - 7.29710456e-08j, - 0.25269477 - 2.29304971e-08j,
                                 - 0.22498386 + 5.78360357e-08j, - 0.05431262 + 3.81051915e-08j,
                                 0.19315448 - 2.65532931e-07j, 0.1771351 - 4.26608723e-07j])

        }
        with self.subTest('check no of bound states'):
            self.assertEqual(self.res['bound_states_num'], 14, "number of bound states not as expected")
        with self.subTest('check contspec 1'):
            self.assertTrue(check_array(self.res['cont_ref1'], expected['cont_ref1']),
                            'contspec (reflection 1) not as expected')
        with self.subTest('check contspec 2'):
            self.assertTrue(check_array(self.res['cont_ref2'], expected['cont_ref2']),
                            'contspec (reflection 2) not as expected')
        with self.subTest('cont_a'):
            self.assertTrue(check_array(self.res['cont_a'], expected['cont_a']), 'contspec (a) not as expected')
        with self.subTest('cont_b1'):
            self.assertTrue(check_array(self.res['cont_b1'], expected['cont_b1']), 'contspec (b1) not as expected')
        with self.subTest('cont_b2'):
            self.assertTrue(check_array(self.res['cont_b2'], expected['cont_b2']), 'contspec (b2) not as expected')


class ManakovvMexExampleTest(unittest.TestCase):
    """Testcase for manakovv_example, (mimic of mex example)."""

    def setUp(self):
        self.res = mex_fnft_manakov_example()

    def test_manakovv_example(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {
            'bound_states_num': 14,
            'bound_states': np.array([-3.56714658e-13 + 0.7695895j, -1.07580611e-12 + 1.76793298j,
                                      5.90749671e-12 + 2.76586856j, -7.94020405e-12 + 3.76381877j,
                                      1.62880820e-12 + 4.76185284j, 5.34070751e+01 + 0.2238525j,
                                      5.34070751e+01 + 1.23470801j, 1.06814150e+02 + 0.7695895j,
                                      -1.06814150e+02 + 1.76793298j, 1.06814150e+02 + 2.76586856j,
                                      -1.06814150e+02 + 4.76185284j, -1.06814150e+02 + 3.76381877j,
                                      -5.34070751e+01 + 1.23470801j, -5.34070751e+01 + 0.2238525j]),
            'cont_ref1': np.array([0.00453788 + 0.00125072j, -0.00314803 + 0.00717911j, 0.02856637 + 0.00118833j,
                                   -0.09057157 - 0.0755944j, 0.02569507 + 0.07997608j, 0.00098114 - 0.00165313j,
                                   -0.0069678 - 0.00333635j, -0.00071609 + 0.00077024j]),
            'cont_ref2': np.array([0.02949623 + 0.00812965j, -0.02046221 + 0.04666421j, 0.1856814 + 0.00772417j,
                                   -0.58871521 - 0.49136358j, 0.16701798 + 0.51984451j, 0.00637742 - 0.01074532j,
                                   -0.04529072 - 0.02168628j, -0.00465457 + 0.00500658j, ]),
            'disc_norm': np.array(
                [0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j])

        }
        with self.subTest('check no of bound states'):
            self.assertEqual(self.res['bound_states_num'], 14, "number of bound states not as expected")
        with self.subTest('check contspec 1'):
            self.assertTrue(check_array(self.res['cont_ref1'], expected['cont_ref1']),
                            'contspec (reflection 1) not as expected')
        with self.subTest('check contspec 2'):
            self.assertTrue(check_array(self.res['cont_ref2'], expected['cont_ref2']),
                            'contspec (reflection 2) not as expected')
        with self.subTest('disc norm'):
            self.assertTrue(check_array(self.res['disc_norm'], expected['disc_norm']), 'disc_norm not as expected')
