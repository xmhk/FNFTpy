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
from examples import kdvv_example, kdvv_example_mex4


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
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']),
                            'bound_states not as expected')
        with self.subTest('disc_norm'):
            self.assertTrue(check_array(self.res['disc_norm'], expected['disc_norm']), 'disc norm not as expected')
        with self.subTest('disc_res'):
            self.assertTrue(check_array(self.res['disc_res'], expected['disc_res']), 'disc res not as expected')
        with self.subTest('check contspec'):
            self.assertTrue(check_array(self.res['cont_ref'], expected['cont_ref']),
                            'contspec (reflection) not as expected')
        with self.subTest('cont_a'):
            self.assertTrue(check_array(self.res['cont_a'], expected['cont_a']), 'contspec (a) not as expected')
        with self.subTest('cont_b'):
            self.assertTrue(check_array(self.res['cont_b'], expected['cont_b']), 'contspec (b) not as expected')


class KdvvExampleTestMex4BoundStates(unittest.TestCase):
    """Testcase for kdvv, check bound states for different discretizations."""

    def setUp(self):
        samplediscretizations = {
            'n2SPLIT2_MODAL_VANILLA': 0,
            'n2SPLIT8A_VANILLA': 18,
            'CF4_3_VANILLA': 23,
            'TES4_VANILLA': 27,
            'BO': 29,
            'n4SPLIT4A': 48,
            'n4SPLIT4B': 49,
            'CF6_4': 53,
            'ES4': 54,
            'TES4': 55}
        M = []
        for kk in samplediscretizations:
            for log2D in [9]:
                res = kdvv_example_mex4(log2D, dis=samplediscretizations[kk], diskey=kk, verbose=False)
                M.append([res['return_value'], res['bound_states'][0], res['bound_states'][1]])
        self.res = np.array(M)

    def test_kdvv_mex4_bound_states(self):
        expectedM = np.array([[0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00030636j, 0.00000000e+00 + 2.99969377j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00030636j, 0.00000000e+00 + 2.99969377j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.j, 0.00000000e+00 + 3.j, ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00000164j, 0.00000000e+00 + 2.99999924j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00030636j, 0.00000000e+00 + 2.99969377j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00000008j, 0.00000000e+00 + 2.99999998j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00000008j, 0.00000000e+00 + 2.99999998j,
                               ],
                              [0.00e+00 + 0.j, 0.00e+00 + 1.j, 0.00e+00 + 3.j, ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00000172j, 0.00000000e+00 + 2.99999858j,
                               ],
                              [0.00000000e+00 + 0.j, 0.00000000e+00 + 1.00000164j, 0.00000000e+00 + 2.99999924j,
                               ]]
                             )

        with self.subTest('check bound states for different discretizations'):
            self.assertTrue(check_array(self.res, expectedM, eps=1e-10),
                            'bound_states (mex 4 examples) not as expected')


class KdvvExampleTestProvideBoundStateGuesses(unittest.TestCase):
    """Testcase for kdvv_example, NEWTON + bound states provided"""

    def setUp(self):
        self.res = kdvv_example(dst=1, cst=3, bsl=0, verbose=False, amplitude_scale=1.3,
                                bsg=[0.1j, 1.j], K=2)
        self.res2 = kdvv_example(dst=1, cst=3, bsl=0, verbose=False, amplitude_scale=1.3,
                                 bsg=[0.1j, 0.01 + 1.j],
                                 K=2)  # should fail, no real part for guesses (yet)

    def test_kdvv_example_bound_states_provided(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {'bound_states': np.array([0. + 0.07454561j, 0. + 1.30818689j])
                    }
        with self.subTest('check bound state results with valid guesses'):
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']),
                            'bound_states not as expected')
        with self.subTest('check bound state results with valid guesses'):
            self.assertTrue(check_array(self.res['bound_states'], expected['bound_states']),
                            'bound_states not as expected')

        self.assertEqual(self.res2['return_value'], 2,
                         "FNFT kdvv return value -- should be 2 if real part of guesses is not zero")
