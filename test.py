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

import numpy as np
from FNFTpy import *


# detect some general errors
#nsevtest()
#kdvvtest()
#nseptest()

# mimic the example files

#kdvvexample()
#nsepexample()
#nsevexample()
#nsevinversetest()

#print_default_options()

def nsevinversetest2():
    from matplotlib import pyplot as plt

    tvec = np.linspace(-15,15,16*128)
    feld = 0.3 / np.cosh(tvec)
    D = len(tvec)
    M = len(tvec)
    res, xi = nsev_inverse_xi_wrapper(D, tvec[0], tvec[-1], M, dis=4)
    print(res, xi)

    res2 = nsev(feld, tvec, xi[0], xi[1], dis=4, cst=2,M=M)
    print(res2.keys())
    contspec = res2['cont_ref']
    print(len(contspec))
    boundstates=None
    normres=None
    kappa=1
    options = get_nsev_inverse_options()
    res3 = nsev_inverse_wrapper(M, contspec, xi[0], xi[1],0,boundstates, normres,
                                D, tvec[0], tvec[-1],
                                kappa, options)
    opts2 = get_nsev_inverse_options(cst=1)
    contspec=res2['cont_b']
    res4 = nsev_inverse_wrapper(M, contspec, xi[0], xi[1],0,boundstates, normres,
                                D, tvec[0], tvec[-1],
                                kappa, opts2)

    print(res3.keys())
    plt.figure()
    plt.subplot(131)
    plt.plot(np.abs(res3['q']),'o')
    plt.plot(np.angle(res3['q']))
    plt.subplot(132)
    plt.plot(np.abs(feld),'x')
    plt.plot(np.angle(feld),'--')
    plt.subplot(133)
    plt.plot(np.abs(res4['q']),'o')
    plt.plot(np.angle(res4['q']))
    plt.show()


def nsevinversetest3():
    from matplotlib import pyplot as plt

    tvec = np.linspace(-15,15,16*128)
    feld = 2.3 / np.cosh(tvec)
    D = len(tvec)
    M = len(tvec)
    res, xi = nsev_inverse_xi_wrapper(D, tvec[0], tvec[-1], M, dis=4)
    print(res, xi)

    res2 = nsev(feld, tvec, xi[0], xi[1], dis=4, cst=0,M=M, dst=2)
    print(res2.keys())
    contspec = res2['cont_ref']
    print(len(contspec))
    boundstates=res2['bound_states']
    #print("BSN",res2['bound_states_num'])
    normres=res2['disc_norm']
    residues = res2['disc_res']
    print(normres)
    kappa=1
    options = get_nsev_inverse_options(dis=4)
    res3 = nsev_inverse_wrapper(M, contspec, xi[0], xi[1],
                                res2['bound_states_num'],
                                boundstates, normres,
                                D, tvec[0], tvec[-1],
                                kappa, options)
    opts2 = get_nsev_inverse_options(dst=1)
    #contspec=res2['cont_b']
    res4 = nsev_inverse_wrapper(M, contspec, xi[0], xi[1],res2['bound_states_num'],
                                boundstates, residues,
                                D, tvec[0], tvec[-1],
                                kappa, opts2)

    print(res3.keys())
    plt.figure()
    plt.subplot(131)
    plt.plot(np.abs(res3['q']),'o')
    plt.plot(np.angle(res3['q']))
    plt.subplot(132)
    plt.plot(np.abs(feld),'x')
    plt.plot(np.angle(feld),'--')
    plt.subplot(133)
    plt.plot(np.abs(res4['q']),'o')
    plt.plot(np.angle(res4['q']))
    plt.show()


#nsevinversetest2()

#nsevinversetest3()
#help(nsev)

#print_default_options()

#print_nsev_inverse_options()

#nsevinversetest()


tvec = np.linspace(-10,10, 1024)
q = 1.3/np.cosh(tvec)

res = nsev(q, tvec, dst=2, cst=2)

print(res.keys())

from matplotlib import pyplot as plt

plt.figure()

def plri(x):
    plt.plot(np.real(x), np.imag(x))
def plap(x):
    plt.plot(np.abs(x))
    plt.plot(np.angle(x),'--')

plt.subplot(231)
plri(res['cont_ref'])
plt.subplot(234)
plap(res['cont_ref'])

plt.subplot(232)
plri(res['cont_a'])
plt.subplot(235)
plap(res['cont_a'])

plt.subplot(233)
plri(res['cont_b'])
plt.subplot(236)
plap(res['cont_b'])
#plt.plot(np.abs(res['cont_ref']))
#plt.plot(np.angle(res['cont_ref']))
#plt.plot(np.real(res['cont_ref']), np.imag(res['cont_ref']))
print(res['cont_b'])
plt.show()