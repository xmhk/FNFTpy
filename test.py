import numpy as np
from FNFTpy import *

# nsepexample()


# ("bound_state_filtering", ctypes_int),
#        ("bound_state_localization", ctypes_int),
#        ("niter", ctypes_uint),
#        ("discspec_type", ctypes_int),
#        ("contspec_type", ctypes_int),
#        ("normalization_flag", ctypes_int32),
#        ("discretization", ctypes_int)]


# detect some general errors
nsevtest()
kdvvtest()
nseptest()

# mimic the example files

print_nsev_options()
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