import numpy as np
#from FNFTpy import *


# detect some general errors
#nsevtest()
#kdvvtest()
#nseptest()

# mimic the example files


# nsevexample()
#kdvvexample()
#nsepexample()
#nsevexample()

# o2 = nsev_default_opts()
# o2.bound_state_localization = 0
# print_nsev_opts(o2)

#options = get_kdvv_options()
#print(repr(options))

#options = get_nsep_options()
#print(repr(options))

#options = get_nsev_options()
#print(repr(options))


#o1 = get_nsep_options()
#o2 = get_nsep_options(loc=0)
#print_nsev_options(opts=o1)
#print_nsev_options(opts=o2)
import numpy as np
from FNFTpy import kdvv, print_kdvv_options
print("\n\nKDVV example")
print("standard options used:")
print_kdvv_options()
print("")
D = 256
tvec = np.linspace(-1, 1, D)
q = np.zeros(D, dtype=np.complex128)
q[:] = 2.0 + 0.0j
Xi1 = -2
Xi2 = 2
M = 8
Xivec = np.linspace(Xi1, Xi2, M)
res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2)
print("FNFT return value: %d (should be 0)" % res['return_value'])
for i in range(len(res['contspec'])):
    print("%d. Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))