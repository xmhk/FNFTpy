

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
import numpy as np

from .external import HiddenPrints


class FnftpyTest():
    """Run some sample code, store and print results."""
    def __init__(self, f_example_code, f_test, verbose=False):
        #self.logstr = ""
        #self.verbose = verbose
        self.testlog = []
        self.tests_total = 0
        self.tests_failed = 0
        if not verbose:
            with HiddenPrints():
                self.res = f_example_code()
        else:
            self.res = f_example_code()
        tmp = f_test(self.res)
        self.testlog = tmp.testlog
        self.tests_failed = tmp.tests_failed
        self.tests_total = tmp.tests_total

    def print_test_result(self, brief=False):
        #print(".. %s"%self.infostr)
        if not brief:
            print("\n passed?")
            for resitem in self.testlog:
                print("  %r   %s"%(resitem[1],resitem[0]))
            print("\n")
        print("%d / %d passed"%(self.tests_total-self.tests_failed,self.tests_total))



