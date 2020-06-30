# FNFTpy - a wrapper for FNFT

This module provides a python interface (wrapper functions) for [FNFT](https://github.com/FastNFT), 
a library for the numerical computation of nonlinear Fourier transforms.

For FNFTpy to work, a copy of FNFT has to be installed.
For general information, source files and installation of FNFT,
visit FNFT's github page: [https://github.com/FastNFT](https://github.com/FastNFT)


## current state - access functions from FNFT version 0.3.0

last update of FNFTpy: 07.03.2020

for changes see [Changelog](CHANGELOG.md)


### Korteweg-de-Fries equation with vanishing boundary conditions:
  * Currently, the continuous spectrum can be calculated.
  * Function **kdvv**: 
    * easy-to-use Python function, options can be passed as optional arguments 
    * minimal example:
        ```
        import numpy as np
        from FNFTpy import kdvv
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
        ```
    * for full description call ```help(kdvv)```
      
      
  * function **kdvv_wrapper**:
    * mimics the function fnft_kdvv from FNFT.
    * for full description call ```help(kdvv_wrapper)```
      
        
  
### Nonlinear Schroedinger Equation with periodic boundary conditions
  * The main and auxiliary spectra can be calculated.
  * Function **nsep**: 
    * easy-to-use Python function, options can be passed as optional arguments 
    * minimal example:
      ```
      import numpy as np
      from FNFTpy import nsep
      print("\n\nnsep example")
      # set values
      D = 257
      tvec = np.linspace(0, 2*np.pi, D)
      q = np.exp(2.0j * tvec)
      # call function
      res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1, kappa=1)
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

       ```
   * for full description call ```help(nsep)```
  * Function **nsep_wrapper**:
    * mimics the function fnft_nsep from FNFT.
    * for full description call ```help(nsep_wrapper)```
     
  
### Nonlinear Schroedinger Equation with vanishing boundary conditions:
  * The discrete and continuous spectra can be calculated.
  * Function **nsev**:
    * easy-to-use Python function, options can be passed as optional arguments 
    
    * minimal example:
        ```
        import numpy as np
        from FNFTpy import nsev
    
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
        ```
    * for full description call ```help(nsev)```
        
  * Function **nsev_wrapper**:
    * mimics the function fnft_nsev from FNFT.
    * for full description call ```help(nsev_wrapper)```
     
### Nonlinear Schroedinger Equation with vanishing boundary conditions (Inverse Transformation): 
 * Perform the Inverse Nonlinear Fourier transform: the temporal field is calculated from the nonlinear spectrum.
 * the continuous part and (optional) the discrete part of the spectrum can be given.  

 * function **nsev_inverse**
    * easy-to-use Python function, options can be passed as optional arguments 
    * minimal example:
         ```
         from FNFTpy import nsev_inverse, nsev_inverse_xi_wrapper
        import numpy as np
        
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
        
        # compare result to analytic function
        print("\n\nnsev-inverse example: Satsuma-Yajima N=2.2")
        print("Difference analytic - numeric: sum((q_ana-q_num)**2) = %.2e  (should be approx 0) "%np.sum(np.abs(q-res['q'])**2))        
         ```
         
  * Function **nsev_inverse_wrapper**:
    * mimics the function fnft_nsev_inverse from FNFT.
    * for full description call ```help(nsev_inverse_wrapper)```
# Requirements
 * Python 3
 * additional Python module: NumPy (python-numpy)  
 
# Setup
 * you may install FNFTpy locally using **pip**:
   From within the project root folder run
     ```
     pip install .     # Install system wide
     pip install -e .  # Install in editable/development mode
     ```

 * **alternatively**, you may add the FNFTpy folder to your Python path.

 * Of course, you need a compiled version of the FNFT C-library. See the
  [documentation for FNFT](https://github.com/FastNFT/FNFT) on how to build 
   the library on your device. 
 * FNFTpy needs to know where the C-library is located. 
   This configuration can be done by editing the function get_lib_path()
   in auxiliary.py. 
   
   Example:
    ```   
    def get_lib_path():
        """Return the path of the FNFT file.
    
        Here you can set the location of the compiled library for FNFT.
        See example strings below.
    
        Returns:
    
        * libstring : string holding library path
    
        Example paths:
    
            * libstr = "C:/Libraries/local/libfnft.dll"  # example for windows            
            * libstr = "/usr/local/lib/libfnft.so"  # example for linux
    
        """
        libstr = "/usr/local/lib/libfnft.so"  # example for linux
        return libstr        
    ```
    
    
 # License 
  
FNFTpy is provided under the terms of the [GNU General Public License, version 2.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

# Contact and contribution

* for bug reports, please use the github issue tracker

* contributors: 

    * Christoph Mahnke (chmhnk_at_googlemail_dot_com)
    * Shrinivas Chimmalgi
    * Simone Gaiarin / simgunz [https://github.com/simgunz]