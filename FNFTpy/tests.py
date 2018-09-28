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


def kdvvexample():
    """Mimics the C example for calling fnft_kdvv."""
    print("\n\nkdvv example")

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
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("continuous spectrum: ")
    for i in range(len(res['cont'])):
        print("%d : Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i],
              np.real(res['cont'][i]), np.imag(res['cont'][i])))


def nsepexample():
    """Mimics the C example for calling fnft_nsep."""
    print("\n\nnsep example")

    # set values
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)

    # call function
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)

    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("number of samples: %d" % D)
    print('main spectrum')
    for i in range(res['K']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                     np.imag(res['main'][i])))
    print('auxiliary spectrum')
    for i in range(res['M']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                     np.imag(res['aux'][i])))


def nsevexample():
    """Mimics the C example for calling fnft_nsev."""
    print("\n\nnsev example")

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
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")

    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['cont_ref'])):
        print("%d :  Xi = %.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['cont_ref'][i]), np.imag(res['cont_ref'][i])))
    print("discrete spectrum")
    for i in range(len(res['bound_states'])):
        print("%d : %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                 np.imag(res['bound_states'][i]),
                                                                 np.real(res['disc_norm'][i]),
                                                                 np.imag(res['disc_norm'][i])))


def nsevinverseexample():
    """Mimics the C example for calling fnft_nsev_inverse."""
    print("\nnsev inverse example")

    # set values
    M = 2048
    K = 0
    D = 1024
    tvec = np.linspace(-2, 2, D)
    T1 = tvec[0]
    T2 = tvec[-1]
    alpha = 2.0
    beta = -0.55
    kappa = 1
    bound_states = None
    normconst_or_residues = None

    # get the frequency intervall suited for the given time vector
    rv, XI = nsev_inverse_xi_wrapper(D, T1, T2, M)
    Xi1 = XI[0]
    Xi2 = XI[1]
    xivec = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)
    contspec = alpha / (xivec - beta * 1.0j)

    # call function
    res = nsev_inverse(xivec, tvec, contspec, None, None)

    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("Total number of samples calculated: %d" % D)
    print("some samples:")
    for i in range(0, D, 64):
        print("  %d : q(t=%.5f) = %.5e + %.5e j " % (i, tvec[i],
                                                     np.real(res['q'][i]),
                                                     np.imag(res['q'][i])))


def nsevinverseexample2():
    """nsev_inverse_example: create a N=2.2 Satsuma-Yajima pulse from nonlinear spectrum."""
    D = 1024
    M = 2*D
    Tmax = 15
    tvec = np.linspace(-Tmax, Tmax, D)
    # calculate suitable frequency bonds (xi)
    rv, xi = nsev_inverse_xi_wrapper(D, tvec[0], tvec[-1], M)
    xivec = xi[0] + np.arange(M) * (xi[1] - xi[0]) / (M - 1)

    # analytic field: chirp-free N=2.2 Satsuma-Yajima pulse
    q = 2.2 / np.cosh(tvec)

    # semi-analytic nonlinear spectrum
    bound_states = np.array([0.7j, 1.7j])
    disc_norming_const_ana = [1.0, -1.0]
    cont_b_ana = 0.587783 / np.cosh(xivec * np.pi) * np.exp(1.0j * np.pi)

    # call the function
    res = nsev_inverse(xivec, tvec, cont_b_ana, bound_states, disc_norming_const_ana, cst=1, dst=0)
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")

    print("FNFT return value: %d (should be 0)" % res['return_value'])
    # compare result to analytic function
    print("\n\nnsev-inverse example: Satsuma-Yajima N=2.2")
    print("Difference analytic - numeric: sum((q_ana-q_num)**2) = %.2e  (should be approx 0) "%np.sum(np.abs(q-res['q'])**2))


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

