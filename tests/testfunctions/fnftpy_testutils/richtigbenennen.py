import numpy as np
from .external import HiddenPrints

class FnftpyTest():
    """Run some sample code, store and print results."""
    def __init__(self, f_example_code, f_test, verbose=False):
        #self.logstr = ""
        #self.verbose = verbose
        self.infostr = ""
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
        self.infostr = tmp.infostr

    def print_test_result(self, brief=False):
        print("\n%s"%self.infostr)
        if not brief:
            print("  passed?")
            for resitem in self.testlog:
                print("  %r   %s"%(resitem[1],resitem[0]))
        print("  %d/%d passed"%(self.tests_total-self.tests_failed,self.tests_total))





class Richtigbenennen():
    def __init__(self, infostr=""):
        self.tests_total = 0
        self.tests_failed = 0
        self.testlog = []
        self.infostr=infostr

    def single_test(self, func, arg1, arg2, infostring):
        self.tests_total+=1
        retv = func(arg1, arg2)
        if not retv:
            self.tests_failed+=1
        self.testlog.append([infostring, retv])

    def check_value(self, value, expectedval):
        return value == expectedval

    def check_array(self, value, expectedval, eps=1e-10):
        # print(np.sum(np.abs(value-expectedval)**2))
        return np.sum(np.abs(value - expectedval) ** 2) < eps

    def check_boolarray(self, value, expectedval):
        return (value == expectedval).all()