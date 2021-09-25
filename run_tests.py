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
from testfunctions import KdvvExampleTest, KdvvExampleTestProvideBoundStateGuesses, \
    KdvvExampleTestMex4BoundStates, \
    NsepExampleTest, NsevExampleTest, NsevExampleTestBoundStateGuesses, NsevExampleTestBoundStateGuessesMex4, NsevExampleTestRF,\
    NsevDstCstInputTest, NsevInverseExample, NsevInverseExample2,NsevInverseExampleMex1, \
    NsevInverseInputVariation, FnftpyOptionsTest
from FNFTpy import print_fnft_version

options_suite = unittest.TestLoader().loadTestsFromTestCase(FnftpyOptionsTest)

kdvv_suite = unittest.TestLoader().loadTestsFromTestCase(KdvvExampleTest)
kdvv_bound_states_mex4 = unittest.TestLoader().loadTestsFromTestCase(KdvvExampleTestMex4BoundStates)
kdvv_newton_bound_suite = unittest.TestLoader().loadTestsFromTestCase(KdvvExampleTestProvideBoundStateGuesses)

nsep_suite = unittest.TestLoader().loadTestsFromTestCase(NsepExampleTest)

nsev_suite1 = unittest.TestLoader().loadTestsFromTestCase(NsevExampleTest)
nsev_suite2 = unittest.TestLoader().loadTestsFromTestCase(NsevDstCstInputTest)
nsev_suite3 = unittest.TestLoader().loadTestsFromTestCase(NsevExampleTestBoundStateGuesses)
nsev_suite4 = unittest.TestLoader().loadTestsFromTestCase(NsevExampleTestBoundStateGuessesMex4)
nsev_suite5 = unittest.TestLoader().loadTestsFromTestCase(NsevExampleTestRF)

# nsev_slow_suite = unittest.TestLoader().loadTestsFromTestCase(NsevSlowExampleTest)

nsev_inverse_suite1 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseExample)
nsev_inverse_suite2 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseExample2)
nsev_inverse_suite3 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseExampleMex1)
nsev_inverse_suite4 = unittest.TestLoader().loadTestsFromTestCase(NsevInverseInputVariation)

suite = unittest.TestSuite([options_suite,
                            kdvv_suite,
                            kdvv_bound_states_mex4,
                            kdvv_newton_bound_suite,
                            nsep_suite,
                            nsev_suite1,
                            nsev_suite2,
                            nsev_suite3,
                            nsev_suite4,
                            nsev_suite5,
                            nsev_inverse_suite1,
                            nsev_inverse_suite2,
                            nsev_inverse_suite3,
                            nsev_inverse_suite4
                            ])

print_fnft_version()
print(
    "\n Note: some output for 'FNFT errors' are intended. This is to check whether errors are catched\n\n")
t1 = unittest.TextTestRunner(buffer=True, verbosity=5).run(suite)
