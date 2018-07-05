import numpy as np
from FNFTpy import *


# detect some general errors
#nsevtest()
#kdvvtest()
#nseptest()

# mimic the example files


# nsevexample()
kdvvexample()
nsepexample()
nsevexample()

# o2 = nsev_default_opts()
# o2.bound_state_localization = 0
# print_nsev_opts(o2)

#options = get_kdvv_options()
#print(repr(options))

#options = get_nsep_options()
#print(repr(options))

#options = get_nsev_options()
#print(repr(options))


o1 = get_nsep_options()
o2 = get_nsep_options(loc=0)
print_nsev_options(opts=o1)
print_nsev_options(opts=o2)