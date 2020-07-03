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

Christoph Mahnke, 2020

"""

import unittest

from .array_test import *
from examples import nsev_slow_example
from FNFTpy import nsev_slow


class NsevSlowExampleTest(unittest.TestCase):
    """Testcase for nsev_slow_example, (mimic of C example)."""

    def setUp(self):
        self.res = nsev_slow_example()
        self.expected = {'bound_states': np.array([0.+1.57422601j]),
                         'disc_norm': np.array([-1.-0.j]),
                         'cont_ref': np.array(
                             [-0.10538565-0.42577137j,
                              -0.78378026-1.04297186j,
                              -1.09090438-1.33957378j,
                              -1.16918546-0.48325228j,
                              -1.16918546+0.48325228j,
                              -1.09090438+1.33957378j,
                              -0.78378026+1.04297186j,
                              -0.10538565+0.42577137j
                              ])}

    def test_nsev_slow_example(self):
        with self.subTest('check FNFT nsev_slow return value'):
            self.assertEqual(self.res['return_value'], 0, "FNFT nsev_slow return value not 0")
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

