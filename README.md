# FNFTpy - a wrapper for FNFT

This module contains wrapper functions for [FNFT](https://github.com/FastNFT), a C library which allows to calculate
the Nonlinear Fourier Transform of some input field.

## current state - access functions from FNFT 0.1.1


### Korteweg-de-Fries equation with vanishing boundary conditions:
  * currently, only the continuous spectrum is calculated
  * function **kdvv**: 
    * easy-to-use python function. Options can be passed by optinal arguments 
    * minimal example:
        ```
        import numpy as np
        from FNFTpy import kdvv, print_kdvv_options
        print("\n\nKDVV example")
        print("standard options used:")
        print_kdvv_options()
        print("")
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(D, dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        Xi1 = -2
        Xi2 = 2
        M = 8
        Xivec = np.linspace(Xi1, Xi2, M)
        res = kdvv(q, tvec, M, Xi1=Xi1, Xi2=Xi2)
        print("FNFT return value: %d (should be 0)" % res['return_value'])
        for i in range(len(res['contspec'])):
            print("%d. Xi=%.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['contspec'][i]), np.imag(res['contspec'][i])))
        ```
    * for full description of options call
        ```
        help(kdvv)
        ```
      
      
  * function **kdvv_wrapper**:
    * mimics the function fnft_kdvv from FNFT.
    * for full description of options call
      ```
        help(kdvv_wrapper)
        ```
      
        
  
### Nonlinear Schroedinger Equation with periodic boundary conditions
  * the main and auxiliary spectra can be calculated
  * function **nsep**: 
    * easy-to-use python function. Options can be passed by optinal arguments 
    * minimal example:
      ```
      import numpy as np
      from FNFTpy import nsep, print_nsep_options
      print("\n\nNSEP example")
      print("standard options used:")
      print_nsep_options()
      print("")
      D = 256
      dt = 2 * np.pi / D
      tvec = np.arange(D) * dt
      q = np.exp(2.0j * tvec)
      res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
      print("FNFT return value: %d (should be 0)" % res['return_value'])
      print("number of samples: %d" % D)
      print('main spectrum')
      for i in range(res['K']):
          print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
      print('auxiliary spectrum')
      for i in range(res['M']):
          print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))

       ```
   * for full description of options call
        ```
        help(nsep)
        ```
  * function **nsep_wrapper**:
    * mimics the function fnft_nsep from FNFT.
    * for full description of options call
      ```
        help(nsep_wrapper)
        ```
     
  
### Nonlinear Schroedinger Equation with vanishing boundary conditions:
  * the discrete and continuous spectra can be calculated
  * function **nsev**:
    * easy-to-use python function. Options can be passed by optinal arguments 
    
    * minimal example:
        ```
        import numpy as np
        from FNFTpy import nsev, print_nsev_options
        print("\n\nNSEV example")
        print("standard options used:")
        print_nsev_options()
        print("")
        D = 256
        tvec = np.linspace(-1, 1, D)
        q = np.zeros(len(tvec), dtype=np.complex128)
        q[:] = 2.0 + 0.0j
        M = 8
        res = nsev(q, tvec, M=M, Xi1=-2, Xi2=2)
        Xivec = np.linspace(-2, 2, M)
        print("FNFT return value: %d (should be 0)" % res['return_value'])
        print("continuous spectrum")
        for i in range(len(res['c_ref'])):
            print("%d Xi = %.4f   %.6f  %.6fj" % (i, Xivec[i], np.real(res['c_ref'][i]), np.imag(res['c_ref'][i])))
        print("discrete spectrum")
        for i in range(len(res['bound_states'])):
            print("%d %.6f  %.6fj with norming const %.6f  %.6fj" % (i, np.real(res['bound_states'][i]),
                                                                 np.imag(res['bound_states'][i]),
                                                                 np.real(res['d_norm'][i]),
                                                                 np.imag(res['d_norm'][i])))
        ```
    * for full description of options call
        ```
        help(nsev)
        ```
        
  * function **nsev_wrapper**:
    * mimics the function fnft_nsev from FNFT.
    * for full description of options call
      ```
        help(nsev_wrapper)
        ```
     
  
  
# Requirements
 * python 3
 * additional modules: numpy 
 
# Setup
 * add FNFTpy folder to your python path
 * the module needs to know where the compiled copy of FNFT is located. 
   The configuration is done via editing the function get_lib_path()
   in auxiliary.py. 
   
   Example:
    ```   
    def get_lib_path():
        """Return the path of the FNFT file.
    
        Here you can set the location of the compiled library for FNFT.
        See example strings below.
    
        Returns:
    
            libstring : string holding library path
        """
        libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
        # libstr = "/usr/local/lib/libfnft.so"  # example for linux
        return libstr
    ```