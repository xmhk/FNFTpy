# FNFTpy - a wrapper for libFNFT

This module contains wrapper functions for [libFNFT](https://github.com/FastNFT), a C library which allows to calculate
the Nonlinear Fourier Transform of some input field.

## current state

FNFTpy currently allows to call the following functions from libFNFT:

* Korteweg-de-Fries equation with vanishing boundary conditions:
  * function kdvv: calculate the continuous spectrum
  * minimal example:
       ```
       import numpy as np
       from FNFTpy import kdvv
       D = 256
       tvec = np.linspace(-1,1,D)
       q = np.zeros(D, dtype=np.complex128)
       q[:] = 2.0 + 0.0j
       xi1 = -2
       xi2 = 2
       M = 8
       #
       # call the function
       #
       res = kdvv(q, tvec, M, xi1=xi1, xi2=xi2, DIS=15)
       #
       # print results
       #
       print("libFNFT return value: %d"%res['return_value'])
       for i in range(len(res['contspec'])):
           print("%d   %.6f  %.6fj"%(i, np.real(res['contspec'][i]),np.imag(res['contspec'][i])))
       ```
   * for full description of options call
       ```
       help(kdvv)
       ```
     from inside a python console (after you imported kdvv)
  
* Nonlinear Schroedinger Equation with periodic boundary conditions
  * function nsep: calculate the main and the auxilary spectrum 
  * minimal example:
      ```
      import numpy as np
      from FNFTpy import nsep
      D= 256
      dt = 2*np.pi/D
      tvec = np.arange(D) * dt
      q = np.exp(2.0j * tvec)
      #
      # call the function
      #
      res = nsep(q, 0, 2*np.pi, BB=[-2,2,-2,2], FILT=1)
      #
      # print results
      #
      print("libFNFT return value: %d"%res['return_value'])
      print('main spectrum')
      for i in range(res['K']):
          print("%d   %.6f  %.6fj"%(i, np.real(res['main'][i]),np.imag(res['main'][i])))        
      print('auxilary spectrum')
      for i in range(res['M']):
          print("%d   %.6f  %.6fj"%(i, np.real(res['aux'][i]),np.imag(res['aux'][i])))
      ```
  * for full description of options call
       ```
       help(nsep)
       ```
    from inside a python console (after you imported nsep)
  
* Nonlinear Schroedinger Equation with vanishing boundary conditions:
  * function nsev: calculate the discrete and the continuous spectrum
    with bound states, residues, norming constants and reflection coefficients
  * minimal example:
      ```
      import numpy as np
      from FNFTpy import nsev
      D=256        
      tvec = np.linspace(-1,1,D)
      q = np.zeros(len(tvec), dtype=np.complex128)
      q[:] = 2.0+0.0j
      M = 8
      xi1 = -2
      xi2 = 2
      #
      # call the function
      #
      res = nsev(q, tvec, M=M, xi1=xi1, xi2=xi2, K=D)
      #
      # print results
      #
      print("libFNFT return value: %d"%res['return_value'])
      print("continuous spectrum")
      for i in range(len(res['c_ref'])):
          print("%d   %.6f  %.6fj"%(i, np.real(res['c_ref'][i]),np.imag(res['c_ref'][i])))
      print("discrete spectrum")
      for i in range(len(res['bound_states'])):
          print("%d   %.6f  %.6fj with norming const %.6f  %.6fj"%(i, np.real(res['bound_states'][i]),
                                    np.imag(res['bound_states'][i]),
                                    np.real(res['d_norm'][i]),
                                    np.imag(res['d_norm'][i])))
       ```
  * for full description of options call
       ```
       help(nsev)
       ```
     from inside a python console (after you imported nsev)
  
  
## requirements
 * python 3 is required
 * additional modules: numpy 
 
## installation
 * place the FNFTpy folder inside your python path
 * the module needs to know where the compiled copy of libFNFT is located. 
   The configuration is done via editing the function get_lib_path()
   in the file auxilary.py. Example:
       
   ```
    def get_lib_path():
      """return the path of the libFNFT file
      This is something you have to edit.
      See example strings.
      """
      libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
      #libstr = "/usr/local/lib/libfnft.so"    #example for linux
    return libstr
   ```
