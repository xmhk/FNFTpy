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
from examples import kdvv_example


class KdvvExampleTest(unittest.TestCase):
    """Testcase for kdvv_example, (mimic of C example)."""

    def setUp(self):
        self.res = kdvv_example(dst=2, cst=2)

    def test_kdvv_example(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {'cont_ref': np.array([
            0.15329981 + 0.12203649j, 0.24385425 + 0.09606438j,
            0.12418466 - 0.00838456j, -0.46324501 + 0.20526334j,
            -0.46324501 - 0.20526334j, 0.12418466 + 0.00838456j,
            0.24385425 - 0.09606438j, 0.15329981 - 0.12203649j]),
            'disc_norm': [1. + 0.j],
            'disc_res': [-0. + 1.87932841j],
            'bound_states_num': 1,
            'bound_states': [0. + 1.10047259j],
            'cont_a': [0.63512744 + 0.79783445j, 0.37980347 + 0.96411068j, - 0.06789142 + 1.00554794j,
                       - 0.46989448 + 1.06047321j, - 0.46989448 - 1.06047321j, - 0.06789142 - 1.00554794j,
                       0.37980347 - 0.96411068j, 0.63512744 - 0.79783445j],
            'cont_b': [1.83186799e-15 + 0.19981659j, - 6.21724894e-15 + 0.27158807j,
                       - 1.71321290e-14 + 0.12544287j, - 2.59237076e-14 - 0.58771104j,
                       - 3.12527781e-14 + 0.58771104j, - 2.03691231e-14 - 0.12544287j,
                       - 6.78623824e-15 - 0.27158807j, 4.08006962e-15 - 0.19981659j]
        }
        with self.subTest('check no of bound states'):
            self.assertEqual(self.res['bound_states_num'], 1, "number of bound states")
        with self.subTest('bound_states'):
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']), 'bound_states as expected')
        with self.subTest('disc_norm'):
            self.assertTrue(check_array(self.res['disc_norm'], expected['disc_norm']), 'disc norm as expected')
        with self.subTest('disc_res'):
            self.assertTrue(check_array(self.res['disc_res'], expected['disc_res']), 'disc res as expected')
        with self.subTest('check contspec'):
            self.assertTrue(check_array(self.res['cont_ref'], expected['cont_ref']),
                            'contspec (reflection) as expected')
        with self.subTest('cont_a'):
            self.assertTrue(check_array(self.res['cont_a'], expected['cont_a']), 'contspec (a) as expected')
        with self.subTest('cont_b'):
            self.assertTrue(check_array(self.res['cont_b'], expected['cont_b']), 'contspec (b) as expected')


class KdvvExampleTest_provide_bound_states(unittest.TestCase):
    """Testcase for kdvv_example, NEWTON + bound states provided"""

    def setUp(self):
        self.res = kdvv_example(dst=1, cst=3, bsl=0, verbose=False, amplitude_scale=1.3,
                                bound_state_guesses=[0.1j, 1.j], K=2)
        self.res2 = kdvv_example(dst=1, cst=3, bsl=0, verbose=False, amplitude_scale=1.3,
                                 bound_state_guesses=[0.1j, 0.01 + 1.j],
                                 K=2)  # should fail, no real part for guesses (yet)

    def test_kdvv_example_bound_states_provided(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {'bound_states': np.array([0. + 0.07454561j, 0. + 1.30818689j])
                    }
        with self.subTest('check bound state results with valid guesses'):
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']), 'bound_states as expected')
        with self.subTest('check bound state results with valid guesses'):
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']), 'bound_states as expected')

        self.assertEqual(self.res2['return_value'], 2,
                         "FNFT kdvv return value -- should be 2 if real part of guesses is not zero")
