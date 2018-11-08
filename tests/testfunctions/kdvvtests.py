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

from .fnftpy_testutils import TestAndAccount
import numpy as np

def kdvv_example_test(res):
    infostr="kdvv (resemble C example)"
    tmp = TestAndAccount(infostr=infostr)

    expected = {'cont': np.array([
        0.15329981+0.12203649j,  0.24385425+0.09606438j,
        0.12418466-0.00838456j, -0.46324501+0.20526334j,
        -0.46324501-0.20526334j,  0.12418466+0.00838456j,
        0.24385425-0.09606438j,  0.15329981-0.12203649j])}
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_array, res['cont'], expected['cont'], "continuous spectrum")
    return tmp