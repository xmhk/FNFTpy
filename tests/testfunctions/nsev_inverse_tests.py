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

from .testobj_class import Testobj
from FNFTpy import nsev_inverse, nsev_inverse_xi_wrapper
import numpy as np

class nsevinverseexample(Testobj):
    """Mimics the C example for calling fnft_nsev_inverse."""
    def example_code(self):

        self.print("\nnsev inverse example")

        # set values
        M = 2048

        D = 1024
        tvec = np.linspace(-2, 2, D)
        T1 = tvec[0]
        T2 = tvec[-1]
        alpha = 2.0
        beta = 0.55
        gamma = np.sqrt( np.abs(alpha)**2 + np.abs(beta)**2)
        kappa = 1

        # get the frequency intervall suited for the given time vector
        rv, XI = nsev_inverse_xi_wrapper(D, T1, T2, M)
        Xi1 = XI[0]
        Xi2 = XI[1]
        xivec = XI[0] + np.arange(M) * (XI[1] - XI[0]) / (M - 1)

        # set continuous spectrum
        contspec = alpha / (xivec - beta * 1.0j)

        # set discrete spectrum
        bound_states = np.array([1.0j * beta])
        normconst_or_residues = np.array([-1.0j * alpha / (gamma + beta)])

        # call function
        res = nsev_inverse(xivec, tvec, contspec, bound_states, normconst_or_residues)

        # print results
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")
        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        self.print("Total number of samples calculated: %d" % D)
        self.print("some samples:")
        for i in range(0, D, 64):
            self.print("  %d : q(t=%.5f) = %.5e + %.5e j " % (i, tvec[i],
                                                         np.real(res['q'][i]),
                                                         np.imag(res['q'][i])))
        res['Xi'] = np.array([Xi1,Xi2])
        self.res =res
    def testconditions(self):
        self.infostr = "Mimic nsev_inverse C example."
        shouldberes = {
            'qsamprange':[0,-1,40],
            'qsamp':
               np.array([-8.51156134e-07-2.59723802e-03j,-8.51152031e-07-5.05389982e-03j,
                        -8.51152828e-07-9.77009846e-03j, -8.51153739e-07-1.88124421e-02j,
                        -8.51154704e-07-3.61352219e-02j, -8.51155662e-07-6.93026882e-02j,
                         -8.51156430e-07-1.32772848e-01j, -8.51156724e-07-2.54100125e-01j,
                         -8.51156012e-07-4.85242920e-01j, -8.51152998e-07-9.20351895e-01j,
                         -8.51144440e-07-1.70480071e+00j, -8.51123774e-07-2.91920894e+00j,
                         -8.51093260e-07-4.03290079e+00j, -8.51159989e-07-2.42570391e-03j,
                         -8.51157880e-07-5.62308393e-04j, -8.51156117e-07-4.40370675e-04j,
                         -8.51154654e-07-3.63745902e-04j, -8.51153407e-07-3.03868218e-04j,
                         -8.51152359e-07-2.54859627e-04j, -8.51151499e-07-2.14146911e-04j,
                         -8.51150765e-07-1.80118348e-04j, -8.51150137e-07-1.51591858e-04j,
                         -8.51149618e-07-1.27638782e-04j, -8.51149196e-07-1.07506128e-04j,
                         -8.51148829e-07-9.05737153e-05j, -8.51148517e-07-7.63264783e-05j]),
            'Xi':np.array([-401.33884499, 401.73116058])
                       }
        self.single_test(self.test_value, self.res['return_value'], 0, "FNFT return value")
        self.single_test(self.test_array_value,
                         self.res['q'][shouldberes['qsamprange'][0]:shouldberes['qsamprange'][1]:shouldberes['qsamprange'][2]],
                         shouldberes['qsamp'],"q values")
        self.single_test(self.test_array_value, self.res['Xi'], shouldberes['Xi'], 'Xi')



class nsevinverseexample2(Testobj):
    """nsev_inverse_example: create a N=2.2 Satsuma-Yajima pulse from nonlinear spectrum."""
    def example_code(self):
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
        self.print("\n----- options used ----")
        self.print(res['options'])
        self.print("\n------ results --------")

        self.print("FNFT return value: %d (should be 0)" % res['return_value'])
        # compare result to analytic function
        self.print("\n\nnsev-inverse example: Satsuma-Yajima N=2.2")
        self.print("Difference analytic - numeric: sum((q_ana-q_num)**2) = %.2e  (should be approx 0) "%np.sum(np.abs(q-res['q'])**2))
        self.res = res