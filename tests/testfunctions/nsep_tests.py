from .testobj_class import Testobj
from FNFTpy import nsep
import numpy as np


class nsepexample(Testobj):
    """Mimics the C example for calling fnft_nsep."""
    def run_test(self):
        self.print("\n\nnsep example")
        # set values
        D = 256
        dt = 2 * np.pi / D
        tvec = np.arange(D) * dt
        q = np.exp(2.0j * tvec)
        # call function
        res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")
        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("number of samples: %d" % D)
        self.print('main spectrum')
        for i in range(res['K']):
            self.print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                         np.imag(res['main'][i])))
        self.print('auxiliary spectrum')
        for i in range(res['M']):
            self.print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                         np.imag(res['aux'][i])))
        self.res = res