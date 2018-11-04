from .testobj_class import Testobj
import numpy as np
from FNFTpy import kdvv

class kdvvexample(Testobj):
    """Mimics the C example for calling fnft_kdvv."""
    def run_test(self):
        self.print("\n\nkdvv example")
        # set values
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(D, dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        Xi1 = -2
        Xi2 = 2
        M = 8
        Xivec = np.linspace(Xi1, Xi2, M)
        # call function
        res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2)
        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")
        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("continuous spectrum: ")
        for i in range(len(res['cont'])):
            self.print("%d : Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i],
                  np.real(res['cont'][i]), np.imag(res['cont'][i])))
        self.res = res
