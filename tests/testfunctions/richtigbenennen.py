import numpy as np
class Richtigbenennen():
    def __init__(tmp):
        tmp.tests_total = 0
        tmp.tests_failed = 0
        tmp.testlog = []

    def single_test(tmp, func, arg1, arg2, infostring):
        tmp.tests_total+=1
        retv = func(arg1, arg2)
        if not retv:
            tmp.tests_failed+=1
        tmp.testlog.append([infostring, retv])

    def check_value(tmp, value, expectedval):
        return value == expectedval

    def check_array(tmp, value, expectedval, eps=1e-10):
        # print(np.sum(np.abs(value-expectedval)**2))
        return np.sum(np.abs(value - expectedval) ** 2) < eps

    def check_boolarray(tmp, value, expectedval):
        return (value == expectedval).all()