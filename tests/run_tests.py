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


from examples import *
from testfunctions import *


T1 = FnftpyTest(kdvv_example, kdvv_example_test)
T2 = FnftpyTest(nsep_example, nsep_example_test)
T3 = FnftpyTest(nsev_example, nsev_example_test)
T4 = FnftpyTest(nsev_dstcst_variation, nsev_dstcst_variation_test)
T5 = FnftpyTest(nsev_inverse_example, nsev_inverse_example_test)
T6 = FnftpyTest(nsev_inverse_example2, nsev_inverse_example2_test)
T7 = FnftpyTest(nsev_inverse_input_variation, nsev_inverse_input_variation_test)


totalnum = 0
failednum = 0

printTR=True
brief=False

for T in [T1, T2, T3, T4, T5, T6, T7]:
    totalnum += T.tests_total
    failednum += T.tests_failed
    if printTR:
        T.print_test_result(brief=brief)
print("\n\n Passed: %d / %d"%(totalnum-failednum, totalnum))