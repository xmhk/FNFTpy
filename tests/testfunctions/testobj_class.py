
class Testobj():
    """Run some sample code, store and print results."""
    def __init__(self, verbose=False):
        self.logstr = ""
        self.verbose = verbose
        self.res = None
        self.run_test()

    def print(self, s):
        if len(self.logstr)>0:
            self.logstr+="\n"
        if self.verbose:
            print(s)
        self.logstr += s

    def run_test(self):
        pass