from .testobj_class import Testobj
from FNFTpy import nsev
import numpy as np

class nsevexample(Testobj):
    def run_test(self):
        """Mimics the C example for calling fnft_nsev."""
        self.print("\n\nnsev example")

        # set values
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(len(tvec), dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        M = 8
        Xi1 = -2
        Xi2 = 2
        Xivec = np.linspace(Xi1, Xi2, M)

        # call function
        res = nsev(q, tvec, M=M, Xi1=Xi1, Xi2=Xi2)

        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")

        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("continuous spectrum")
        for i in range(len(res['cont_ref'])):
            self.print("%d :  Xi = %.4f   %.6f  %.6fj" % (
            i, Xivec[i], np.real(res['cont_ref'][i]), np.imag(res['cont_ref'][i])))
        self.print("discrete spectrum")
        for i in range(len(res['bound_states'])):
            self.print("%d : %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                       np.imag(res['bound_states'][i]),
                                                                            np.real(res['disc_norm'][i]),
                                                                            np.imag(res['disc_norm'][i])))
        self.res = res

