## changelog

## current

### August 2023
- implement  'tol' argument for nsev functions
- implement optional 'bb' (bounding box) argument for nsev functions
- implement optional 'gs' (grid_spacing) argument for kdvv

### June 2022

- added tests and additions from FNFT branch nsep-improvements, merged into development

### Sept 2021 - November 2021   0.4.1-dev

- general:
  - updated some docstrings
  - add more tests
  
- **manakovv**: 
  - added interface to the FNFTs manakovv functions

- **kdvv**:
  - following the update if FNFTs kdvv,
    - kdvv now has more options, bound states and discrete spectrum can be calculated
    - initial guesses for bound states can be provided, for newton bound state localization

- **nsev**:
  - implemented that initial guesses can be provided for newton bound state localization
  
## 0.4.1

### 17.01.2022

- introduced an optional argument `display_c_msg` for the main functions `kdvv`, `kdvv_wrapper`, `nsep`, `nsep_wrapper`,
  `nsev`, `nsev_wrapper`, `nsev_inverse`, `nsev_inverse_wrapper` and `nsev_inverse_xi_wrapper`. 
  Default it is set to `true`. If set to `false`, messages from the c-library to stdout are suppressed.

### 28.06.2021
- changed the way how ctypes.CDLL is called.
- Some users (WIN) had problems to load the libfnft.dll file although the proper path was given in _get_lib_path.
  The (somewhat bad) solution introduced is to pass an `winmode=` argument to the CDLL call. It showed that passing '0'
  fixes the bug, so I introduced the function `get_winmode_param()` in `auxiliary.py` which as a standard returns 0.
  If you encounter problems, try setting the return value of this function e.g. to 'None'.


### 08.07.2020 checked for compatibility with FNFT 0.40
- kdvv: updated available discretizations in documentation, phase_shift option available
- nsep: updated available discretizations in documentation
- nsev: updated available discretizations in documentation, richardson extrapolation flag available
- nsev_inverse: updated available discretization in documentation


## 0.3.0

### 07.03.2020
- checked compatibility with FNFT 0.3.0
- merge development into master

## 0.2.2

### 05.03.2020
- adapted small changes in NSEP options/API from FNFT

### 31.10.2019

- introduced setup.py for installation with pip


### 23.12.2018

- checked compliance with FNFT 0.2.2: no changes in code

## 0.2.1

## 19.05.2019
- in dev: numerical value of nsep test output changed slightly - adapted test

### 21.11.2018
- small changes in documentation
- small changes in examples shown in README
  
### 20.11.2018
- moved example functions into separate folder
- added testfunctions to test basic interaction with FNFT
- refactoring according to PEP8
- option structs now have unified __repr__ and __print__ functions

### 08.11.2018
- fix check_return_code output warning
- re-structuring of nsev_inverse_wrapper decision tree (bound states given? contspec given?).
    Should show no effect on existing code and prevents Python crash when none of both is given (FNFT will return 7 and q all zeros in that case).

### 02.11.2018
- nsev, nsev_wrapper:
    - options switch: dst=3 now allows skipping the calculation of the discrete spectrum
    - options switch: cst=3 now allows skipping the calculation of the continuous spectrum
    - order of cst/dst options handling
- nsev_inverse
    - NONE can be passed as continuous spectrum for pure soliton states
- nsev_inverse_wrapper
    - M=0 can be passed to omit continuous spectrum
    
### 15.10.2018
 - small changes in README

### 01.10.2018
- updated nsev_inverse_example to mimic the C example

### 28.09.2018 
- added changelog
- no changes, checked compatibility with FNFT 0.2.1