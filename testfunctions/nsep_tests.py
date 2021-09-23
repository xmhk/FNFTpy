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

import unittest

from .array_test import *
from examples import nsep_example


class NsepExampleTest(unittest.TestCase):
    """Testcase for nsep_example, (mimic of C example)."""

    def setUp(self):
        self.res = nsep_example()
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
            self.assertTrue(check_array(
                np.sort_complex(np.around(self.res['main'], 8)),
                np.sort_complex(self.expected['main']), eps=1e-8
            ), "main spectrum not as expected")
