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
       x1 = -2
       x2 = 2
       M = 8
       res = kdvv(q, tvec, M, xi1=x1, xi2=x2, DIS=15)
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
      res = nsep(q, 0, 2*np.pi, BB=[-2,2,-2,2], FILT=1)
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
      res = nsev(q, tvec, M=M,xi1=-2,xi2=2,K=D ,)
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
 * the module needs to know where the compiled copy of libFNFT is located. This is done via editing the 
   file libFNFT_path.ini inside the FNFTpy folder. Example:
       
   ```
   [libFNFT]
   # this is a comment
   #path=C:/Users/Username/Documents/FNFT/build/libfnft.dll  # for windows
   path=/usr/local/lib/libfnft.so # linux
   ```
