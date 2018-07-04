# import numpy as np
# import ctypes
from .auxiliary import get_lib_path

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper, kdvv
from .fnft_nsep_wrapper import nsep_wrapper,  nsep
from .fnft_nsev_wrapper import nsev_wrapper, nsev
from .typesdef import *
from .options_handling import *

# get python ctypes object of FNFT
#libpath = get_lib_path()  # edit in auxiliary.py
#fnft_clib = ctypes.CDLL(libpath)

