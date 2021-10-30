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
from examples import nsep_example
from FNFTpy import fnft_nsep_loc


class NsepExampleTest(unittest.TestCase):
    """Testcase for nsep_example, (mimic of C example)."""

    def setUp(self):
        self.res = nsep_example()
        # self.res = nsep_example(loc=fnft_nsep_loc.MIXED, maxev=20)
        self.expected = {'main': np.array([1.29133168 + 6.20755497e-09j, 1.29133165 - 2.43783858e-09j,
                                           -0.99999999 - 8.65909596e-01j, -0.99999999 - 8.65909598e-01j,
                                           0.11812379 + 1.39929078e-09j, 0.11812416 - 4.23632405e-07j,
                                           -0.99999999 + 8.65909598e-01j, -0.99999999 + 8.65909598e-01j,
                                           1.82846271 + 1.15271427e-08j, 1.82846267 + 4.17009152e-10j,
                                           0.7321088 + 2.14041300e-09j, 0.73210888 - 1.21983992e-07j,
                                           -0.99999999 - 9.99899604e-01j, -1.01392233 - 4.31204461e-05j,
                                           -1.01441588 + 5.29052866e-05j, -0.98558342 - 5.27110635e-05j,
                                           -0.98607588 + 4.08981616e-05j, -0.99999999 + 9.99899604e-01j]),
                         'aux': np.array([1.82846264 - 2.03421871e-15j, 1.29133168 + 2.31746575e-15j,
                                          0.73210878 - 1.62036153e-15j, 0.11812379 + 1.77918869e-15j,
                                          -0.99999999 - 8.65909474e-01j, -0.99999999 + 8.65909474e-01j])
                         }

    def test_nsep_example(self):
        with self.subTest('check FNFT nsep return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsep return value")
        with self.subTest('check M value'):
            self.assertEqual(self.res['M'], 6, "M not 6")
        with self.subTest('check aux spectrum value'):
            self.assertTrue(check_array(
                np.sort_complex(np.around(self.res['aux'], 8)),
                np.sort_complex(self.expected['aux'])
            ), "aux spectrum not as expected")
        with self.subTest('check K value'):
            self.assertEqual(self.res['K'], 18, "K not 18")
        with self.subTest('check main spectrum value'):
            self.assertTrue(check_array(
                np.sort_complex(np.around(self.res['main'], 8)),
                np.sort_complex(self.expected['main']), eps=1e-8
            ), "main spectrum not as expected")


class NsepExampleTest_priorNewton(unittest.TestCase):
    """Testcase for nsep_example, (mimic of C example).

    results are prior to introductions of Newton localization,
    and can now be achieved with options:  loc= 2 (MIXED) and maxev=20"""

    def setUp(self):
        # self.res = nsep_example()
        self.res = nsep_example(loc=fnft_nsep_loc.MIXED, maxev=20)
        self.expected = {'main': np.array([-1.0 + -0.865909j,
                                           -1.0 + -0.865909j,
                                           -1.0 + 0.865909j,
                                           -1.0 + 0.865909j,
                                           -1.0 + -0.9999j,
                                           -1.0 + 0.9999j,
                                           0.11804 + 6.56651e-08j,
                                           1.29147 + 1.11864e-08j,
                                           -0.999928 + -3.7809e-05j,
                                           0.732246 + -1.84169e-09j,
                                           1.82865 + 1.74943e-08j,
                                           ]),
                         'aux': np.array([
                             - 1.0 + -0.865909j,
                             - 1.0 + 0.865909j,
                             - 0.999939 + 1.87816e-08j,
                             0.118146 + 2.82216e-07j,
                             0.732225 + 1.1282e-08j,
                             1.29152 + 6.35545e-08j,
                             1.82871 + 8.88013e-08j,
                         ])
                         }

    def test_nsep_example(self):
        with self.subTest('check FNFT nsep return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsep return value")
        with self.subTest('check M value'):
            self.assertEqual(self.res['M'], 7, "M not 7")
        with self.subTest('check aux spectrum value'):
            self.assertTrue(check_array(
                np.sort_complex(np.around(self.res['aux'], 8)),
                np.sort_complex(self.expected['aux'])
            ), "aux spectrum not as expected")
        with self.subTest('check K value'):
            self.assertEqual(self.res['K'], 11, "K not 11")
        with self.subTest('check main spectrum value'):
            self.assertTrue(
                np.linalg.norm(self.res['main'] - self.expected['main']) / np.linalg.norm(self.expected['main']) < 7e-5
                , "main spectrum not as expected")
