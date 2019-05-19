## changelog

## 0.2.1

## 19.05.2019
  * in dev: numerical value of nsep test output changed slightly - adapted test

### 21.11.2018
  * small changes in documentation
  * small changes in examples shown in README
  
### 20.11.2018
  * moved example functions into separate folder
  * added testfunctions to test basic interaction with FNFT
  * refactoring according to PEP8
  * option structs now have unified __repr__ and __print__ functions

### 08.11.2018
  * fix check_return_code output warning
  * re-structuring of nsev_inverse_wrapper decision tree (bound states given? contspec given?). 
    Should show no effect on existing code and prevents Python crash when none of both is given (FNFT will return 7 and q all zeros in that case).

### 02.11.2018
  * nsev, nsev_wrapper: 
    * options switch: dst=3 now allows skipping the calculation of the discrete spectrum
    * options switch: cst=3 now allows skipping the calculation of the continuous spectrum
    * order of cst/dst options handling
  * nsev_inverse
    * NONE can be passed as continuous spectrum for pure soliton states
  * nsev_inverse_wrapper
    * M=0 can be passed to omit continuous spectrum
    
### 15.10.2018
  * small changes in README

### 01.10.2018
  * updated nsev_inverse_example to mimic the C example

### 28.09.2018 
  * added changelog
  * no changes, checked compatibility with FNFT 0.2.1