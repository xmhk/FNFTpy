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



#from fnftpy_testutils import *
from examples import *
from testfunctions import *


T = FnftpyTest(nsep_example, nsep_example_test)
T.print_test_result(brief=True)

T2 = FnftpyTest(kdvv_example, kdvv_example_test)
T2.print_test_result(brief=True)

T3 = FnftpyTest(nsev_example, nsev_example_test)
T3.print_test_result(brief=True)

T4 = FnftpyTest(nsev_dstcst_variation, nsev_dstcst_variation_test)
T4.print_test_result(brief=True)

T5 = FnftpyTest(nsev_inverse_example, nsev_inverse_example_test)
T5.print_test_result(brief=True)

T6 = FnftpyTest(nsev_inverse_example2, nsev_inverse_example2_test)
T6.print_test_result(brief=True)


T7 = FnftpyTest(nsev_inverse_input_variation, nsev_inverse_input_variation_test)
T7.print_test_result(brief=False)