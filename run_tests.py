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
from testfunctions import KdvvExampleTest, NsepExampleTest, NsevExampleTest, \
    NsevDstCstInputTest, NsevInverseExample, NsevInverseExample2, \
    NsevInverseInputVariation, FnftpyOptionsTest
from FNFTpy import print_fnft_version

options_suite = unittest.TestLoader().loadTestsFromTestCase(FnftpyOptionsTest)

kdvv_suite = unittest.TestLoader().loadTestsFromTestCase(KdvvExampleTest)

nsep_suite = unittest.TestLoader().loadTestsFromTestCase(NsepExampleTest)

nsev_suite1 = unittest.TestLoader().loadTestsFromTestCase(NsevExampleTest)
nsev_suite2 = unittest.TestLoader().loadTestsFromTestCase(NsevDstCstInputTest)

nsev_inverse_suite1 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseExample)
nsev_inverse_suite2 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseExample2)
nsev_inverse_suite3 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseInputVariation)

suite = unittest.TestSuite([options_suite,
                            kdvv_suite,
                            nsep_suite,
                            nsev_suite1, nsev_suite2,
                            nsev_inverse_suite1,
                            nsev_inverse_suite2,
                            nsev_inverse_suite3
     ])

print_fnft_version()
print("\n\nthe FNFT error ('FNFT Error: Sanity check failed (Neither contspec nor discspec provided.)') is intended: just to check that it is catched without crashing ...\n\n")
t1 = unittest.TextTestRunner(buffer=True, verbosity=1).run(suite)
