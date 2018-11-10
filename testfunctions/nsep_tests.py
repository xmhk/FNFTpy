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
        self.expected = {'aux': np.array([-0.99999999 - 8.65909474e-01j, -0.99999999 + 8.65909474e-01j,
                                          -0.99993896 + 1.87820258e-08j, 0.11814625 + 2.82216353e-07j,
                                          0.73222476 + 1.12819764e-08j, 1.29151798 + 6.35545312e-08j,
                                          1.82871124 + 8.88012865e-08j]),
                         'main': np.array([-0.99999999 - 8.65909473e-01j, -0.99999999 - 8.65909475e-01j,
                                           -0.99999999 + 8.65909475e-01j, -0.99999999 + 8.65909474e-01j,
                                           -0.99999999 - 9.99899604e-01j, -0.99999999 + 9.99899604e-01j,
                                           0.1180403 + 6.56652320e-08j, 1.2914677 + 1.11864992e-08j,
                                           -0.99977766 - 6.49652790e-06j, 0.73224594 - 1.84219275e-09j,
                                           1.8286518 + 1.74944489e-08j])}

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
