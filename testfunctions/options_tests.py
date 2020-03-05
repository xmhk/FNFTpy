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

from FNFTpy import KdvvOptionsStruct, NsepOptionsStruct, NsevInverseOptionsStruct, NsevOptionsStruct, \
    get_kdvv_options, get_nsep_options, get_nsev_options, get_nsev_inverse_options

import unittest


class FnftpyOptionsTest(unittest.TestCase):
    """test whether get_xxx_options return expected values."""

    def setUp(self):
        # remark: third element of lists are one singe string each (print(repr(opts))). They may look confusing
        self.expected = dict(kdvv=[KdvvOptionsStruct, get_kdvv_options, "'discretization' : 17"],
                             nsep=[NsepOptionsStruct, get_nsep_options,
                                    ],

                             nsev=[NsevOptionsStruct, get_nsev_options,
                                            "'bound_state_filtering' : 2, 'bound_state_localization' : 2, 'niter' : 10, 'Dsub' : 0, " \
                                            + "'discspec_type' : 0, 'contspec_type' : 0, 'normalization_flag' : 1, 'discretization' : 11"],
                             nsev_inverse=[NsevInverseOptionsStruct, get_nsev_inverse_options,
                                           "'discretization' : 4, 'contspec_type' : 0, 'contspec_inversion_method' : 0, " \
                                           + "'discspec_type' : 0, 'max_iter' : 100, 'oversampling_factor' : 8"])

    def test_get_options_type(self):
        for k in self.expected.keys():
            opts = self.expected[k][1]()
            with self.subTest('check whether return of get_%s_options is correct Options struct' % k):
                self.assertIsInstance(opts, self.expected[k][0])

    def test_get_options_value(self):
        for k in self.expected.keys():
            opts = self.expected[k][1]()
            with self.subTest('check standard repr of %s' % k):
                self.assertEqual(repr(opts), self.expected[k][2])
