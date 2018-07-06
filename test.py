import numpy as np
from FNFTpy import *


# detect some general errors
#nsevtest()
#kdvvtest()
#nseptest()

# mimic the example files

# kdvvexample()
# nsepexample()
#nsevexample()

#print_default_options()
#nsevtest()

t = NsevInverseOptionsStruct(1,1,1,1,1)

t2 = fnft_nsev_inverse_default_opts_wrapper()

#print(repr(t2))
print_nsev_inverse_options(t)
print("---")
print_nsev_inverse_options(t2)
print("---(default)")
print_nsev_inverse_options()
