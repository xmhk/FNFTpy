# FNFTpy - a wrapper for FNFT

This module contains wrapper functions for [FNFT](https://github.com/FastNFT), a C library which allows to calculate
the Nonlinear Fourier Transform of some input field.

## current state - access functions from FNFT 0.1.1


* Korteweg-de-Fries equation with vanishing boundary conditions:
  * function kdvv: calculate the continuous spectrum
  * minimal example:
    ```
    import numpy as np
    from FNFTpy import kdvv
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(d, dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    xi1 = -2
    xi2 = 2
    m = 8
    xivec = np.linspace(xi1, xi2, m)    
    res = kdvv(q, tvec, m, xi1=xi1, xi2=xi2, dis=15)
    print("FNFT return value: %d" % res['return_value'])
    for i in range(len(res['contspec'])):
        print("%d. xi=%.4f   %.6f  %.6fj" % (i, xivec[i], np.real(res['contspec'][i]), 
                                             np.imag(res['contspec'][i])))
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
      d = 256
      dt = 2 * np.pi / d
      tvec = np.arange(d) * dt
      q = np.exp(2.0j * tvec)
      res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
      print("FNFT return value: %d" % res['return_value'])
      print('main spectrum')
      for i in range(res['k']):
          print("%d   %.6f  %.6fj" % (i, np.real(res['main'][i]), np.imag(res['main'][i])))
      print('auxilary spectrum')
      for i in range(res['m']):
          print("%d   %.6f  %.6fj" % (i, np.real(res['aux'][i]), np.imag(res['aux'][i])))

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
    d = 256
    tvec = np.linspace(-1, 1, d)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.0 + 0.0j
    m = 8
    res = nsev(q, tvec, m=m, xi1=-2, xi2=2, k=d)
    xivec = np.linspace(-2, 2, m)
    print("FNFT return value: %d" % res['return_value'])
    print("continuous spectrum")
    for i in range(len(res['c_ref'])):
        print("%d xi = %.4f   %.6f  %.6fj" % (i, xivec[i], np.real(res['c_ref'][i]), np.imag(res['c_ref'][i])))
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
     from inside a python console (after you imported nsev)
  
  
## requirements
 * python 3 is required
 * additional modules: numpy 
 
## installation
 * place the FNFTpy folder inside your python path
 * the module needs to know where the compiled copy of FNFT is located. 
   The configuration is done via editing the function get_lib_path()
   in the file auxilary.py. Example:
       
   ```
    def get_lib_path():
        """return the path of the FNFT file
        This is something you have to edit.
        See example strings.
        """
        libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
        #libstr = "/usr/local/lib/libfnft.so"    #example for linux
        return libstr
   ```
