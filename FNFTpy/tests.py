"""
This file is part of FNFTpy.
FNFTpy provides wrapper functions to interact with FNFT,
a library for the numerical computation of nonlinear Fourier transforms.

For FNFTpy to work, a copy of FNFT has to be installed.
For general information, source files and installation of FNFT,
visit FNFT's github page: https://github.com/FastNFT

For information about setup and usage of FNFTpy see README.md or documentation.

FNFTpy is free software; you can redistribute it and/or
modify it under the terms of the version 2 of the GNU General
Public License as published by the Free Software Foundation.

FNFTpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Contributors:

Christoph Mahnke, 2018

"""

from .fnft_kdvv_wrapper import *
from .fnft_nsep_wrapper import *
from .fnft_nsev_wrapper import *
from .fnft_nsev_inverse_wrapper import *


def print_default_options():
    """Print the default options for kdvv, nsep, nsev and nsev_inverse."""

    
    kdvvoptions = get_kdvv_options()
    print("\n ----\n kdvv default options:\n %s \n\n"%repr(kdvvoptions))

    nsepoptions = get_nsep_options()
    print("\n ----\n nsep default options:\n %s \n\n" % repr(nsepoptions))

    nsevoptions = get_nsev_options()
    print("\n ----\n nsev default options:\n %s \n\n" % repr(nsevoptions))

    nsevinverseoptions = get_nsev_inverse_options()
    print("\n ----\n nsev inverse default options:\n %s \n\n" % repr(nsevinverseoptions))






def kdvvtest():
    print("KDVV test")
    xvec = np.linspace(-10, 10, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = kdvv(q, xvec)
    print(res['return_value'])
    res = kdvv(q, xvec, Xi1=-10, Xi2=10, dis=15, M=2048)
    print(res['return_value'])


def nseptest():
    print("NSEP test")
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsep(q, 0, 2 * np.pi)
    print(res['return_value'])
    res = nsep(q, 0, 2 * np.pi, maxev=40)
    print(res['return_value'])


def nsevtest():
    print("NSEV test")
    xvec = np.linspace(0, 2 * np.pi, 256)
    q = np.sin(2 * np.pi / 256 * xvec)
    res = nsev(q, xvec, Dsub=32)
    print(res['return_value'])
    #print(res['options'])


def nsevoptionstest():
    """check some options for dst and cst"""
    tvec = np.linspace(-20,20, 1024)
    q = 2.3 / np.cosh(tvec) + 0.0j
    dstopts = [0,1,2,3,33,-1]
    cstopts = [0,1,2,3, 33, -1]
    keys = [ 'disc_norm', 'disc_res', 'cont_ref', 'cont_a', 'cont_b']
    for dd in dstopts:
        for cc in cstopts:
            res = nsev(q, tvec, dst=dd, cst=cc)
            print("\n\n------ d = %d    c  = %d   return_value = %d ------"%(dd,cc, res['return_value']))
            for kk in keys:
                bv = kk in res.keys()
                print("Key exists ? ", kk,"  ", bv)
