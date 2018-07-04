# import numpy as np
# import ctypes
from .auxiliary import get_lib_path

# import wrapper functions
from .fnft_kdvv_wrapper import kdvv_wrapper, kdvv # fnft_kdvv_default_opts_wrapper, kdvv
from .fnft_nsep_wrapper import nsep_wrapper,  nsep #, fnft_nsep_default_opts_wrapper
from .fnft_nsev_wrapper import nsev_wrapper, nsev#  #fnft_nsev_default_opts_wrapper
from .typesdef import *
from .options_handling import *

# get python ctypes object of FNFT
#libpath = get_lib_path()  # edit in auxiliary.py
#fnft_clib = ctypes.CDLL(libpath)

