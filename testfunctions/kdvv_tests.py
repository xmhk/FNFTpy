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
from examples import kdvv_example


class KdvvExampleTest(unittest.TestCase):
    """Testcase for kdvv_example, (mimic of C example)."""

    def setUp(self):
        self.res = kdvv_example()

    def test_kdvv_example(self):
        with self.subTest('check FNFT kdvv return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT kdvv return value")
        expected = {'cont_ref': np.array([
            0.15329981 + 0.12203649j, 0.24385425 + 0.09606438j,
            0.12418466 - 0.00838456j, -0.46324501 + 0.20526334j,
            -0.46324501 - 0.20526334j, 0.12418466 + 0.00838456j,
            0.24385425 - 0.09606438j, 0.15329981 - 0.12203649j])}
        with self.subTest('check contspec'):
            self.assertTrue(check_array(self.res['cont_ref'], expected['cont_ref']), 'contspec as expected')
