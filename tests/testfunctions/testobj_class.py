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

class Testobj():
    """Run some sample code, store and print results."""
    def __init__(self, verbose=False):
        self.logstr = ""
        self.verbose = verbose
        self.res = None
        self.example_code()
        self.tests_total = 0
        self.tests_failed = 0
        self.testlog=[]
        self.infostr=""
        self.testconditions()

    def print(self, s):
        if len(self.logstr)>0:
            self.logstr+="\n"
        if self.verbose:
            print(s)
        self.logstr += s

    def print_test_result(self):
        print("---- test: %s ----"%self.infostr)
        print("\n passed?")
        for resitem in self.testlog:
            print("  %r   %s"%(resitem[1],resitem[0]))
        print("\n %d / %d passed"%(self.tests_total-self.tests_failed,self.tests_total))
    def example_code(self):
        pass

    def single_test(self, func, arg1, arg2, infostring):
        self.tests_total+=1
        retv = func(arg1, arg2)
        if not retv:
            self.tests_failed+=1
        self.testlog.append([infostring, retv])

    def test_value(self, value, expectedval):
        return value == expectedval

    def test_array_value(self, value, expectedval, eps=1e-10):
        #print(np.sum(np.abs(value-expectedval)**2))
        return np.sum(np.abs(value-expectedval)**2) < eps

    def key_is_in_list(self, key, keylist):
        return key in keylist
