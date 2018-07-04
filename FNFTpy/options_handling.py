from .auxiliary import get_lib_path, check_value
from .typesdef import *

# ------------------------------------------------------------------------------------

def fnft_kdvv_default_opts_wrapper():
    """
    Call the default options for kdvv directly from the library
    Returns:
        KdvvOptionsStruct: holding default options
    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_kdvv_default_opts

    clib_func.restype = KdvvOptionsStruct
    clib_func.argtpes=[]
    return clib_func()

def print_kdvv_options(opts = None):
    if opts is None:
        opts = fnft_kdvv_default_opts_wrapper()
    print("kdvv options:")
    print("   dis", opts.discretization)


def get_kdvv_options(dis=None):
    """returns an options struct for KDVV
    Parameters:
    ----------
        dis: discretization [optional]
               0 = 2SPLIT1A
               1 = 2SPLIT1B
               2 = 2SPLIT2A
               3 = 2SPLIT2B
               4 = 2SPLIT3A
               5 = 2SPLIT3B
               6 = 2SPLIT4A
               7 = 2SPLIT4B
               8 = 2SPLIT5A
               9 = 2SPLIT5B
               10 = 2SPLIT6A
               11 = 2SPLIT6B
               12 = 2SPLIT7A
               13 = 2SPLIT7B
               14 = 2SPLIT8A
               15 = 2SPLIT8B
    Returns:
    ----------
        options struct for KDVV C call
    """
    opts = fnft_kdvv_default_opts_wrapper()
    if not dis is None:
        check_value(dis, 0, 15)  # Discretization
        opts.discretization = dis
    return opts


# -----------------------------------------------------------

def fnft_nsep_default_opts_wrapper():
    """
        Call the default options for nsep directly from the library
        Returns:
            NsepOptionsStruct: holding default options
        """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsep_default_opts
    clib_func.restype = NsepOptionsStruct
    clib_func.argtpes=[]
    return clib_func()


def print_nsep_options(opts = None):
    if opts is None:
        opts = fnft_nsep_default_opts_wrapper()
    print("nsep options:")
    print("    loc", opts.localization)
    print("    filt", opts.filtering)
    print("    bb", opts.bounding_box[0], opts.bounding_box[1], opts.bounding_box[2], opts.bounding_box[3])
    print("    maxev", opts.max_evals)
    print("    dis", opts.discretization)
    print("    nf flag", opts.normalization_flag)


def get_nsep_options(loc=None, filt=None, bb=None, maxev=None, dis=None, nf=None):
    """creates a options struct for NSEP
    Parameters:
    ----------
        loc : localization of spectrum
                0=Subsample and Refine
                1=Gridsearch
                2=Mixed
        filt : filtering of spectrum
                 0=None
                 1=Manual
                 2=Auto
        bb : bounding box used for manual filtering
        maxev : maximum number of evaluations for root refinement
        nf : normalization flag
        dis : discretization
                0=2split2modal
                1=2split2a
                2=2split4a
                3=2split4b
                4=BO
    Returns:
    ----------
        options struct  for NSEP C call
    """
    opts = fnft_nsep_default_opts_wrapper()
    if not loc is None:
        check_value(loc, 0, 2)  # Bound state loclization
        opts.localization = loc
    if not filt is None:
        check_value(filt, 0, 2)  # Bound state localization
        opts.filtering = filt
    if not nf is None:
        check_value(nf, 0, 1)  # Normflag
        opts.normalization_flag = nf
    if not dis is None:
        check_value(dis, 0, 4)  # Discretization
        opts.discretization = dis
    if not bb is None:
        #bbtype = 4 * ctypes_double
        opts.bounding_box[0] = bb[0]
        opts.bounding_box[1] = bb[1]
        opts.bounding_box[2] = bb[2]
        opts.bounding_box[3] = bb[3]
    if not maxev is None:
        opts.max_evals = maxev
    return opts


# -----------------------------------------------------------




def fnft_nsev_default_opts_wrapper():
    """
    Call the default options for nsev directly from the library
        Returns:
            NsevOptionsStruct: holding default options
    """
    fnft_clib = ctypes.CDLL(get_lib_path())
    clib_func = fnft_clib.fnft_nsev_default_opts
    clib_func.restype = NsevOptionsStruct
    clib_func.argtpes=[]
    return clib_func()

def print_nsev_options(opts = None):
    if opts is None:
        opts =  fnft_nsev_default_opts_wrapper()
    print("nsev options:")
    print("    bsf", opts.bound_state_filtering)
    print("    bsl", opts.bound_state_localization)
    print("    niter", opts.niter)
    print("    dst", opts.discspec_type)
    print("    cst", opts.contspec_type)
    print("    dis", opts.discretization)
    print("    nf", opts.normalization_flag)


def get_nsev_options(bsf=None, bsl=None, niter=None, dst=None, cst=None, nf=None, dis=None):
    """creates a options struct for NSEV
    Parameters:
    ----------
        bsf : bound state filtering
                0=none
                1=basic
                2=full
        bsl : bound state localization
                0=Fast Eigenvalue
                1=Newton
                2=Subsample and Refine
        niter : number of iterations for Newton bound state location
        dst : type of discrete spectrum
                 0=norming constants
                 1=residues
                 2=both
        cst : type of continuous spectrum
                 0=reflection coefficient
                 1=a and b
                 2=both
        nf : normalization Flag 0=off, 1=on
        dis : discretization
               0=2split2modal
               1=2split2a
               2=2split4a
               3=2split4b
               4=BO
    Returns:
    ----------
        options struct  for NSEV C call
    """
    opts =  fnft_nsev_default_opts_wrapper()
    if not bsf is None:
        check_value(bsf, 0, 2)  # Bound state filtering
        opts.bound_state_filtering = bsf
    if not bsl is None:
        check_value(bsl, 0, 2)  # Bound state localization
        opts.bound_state_localization = bsl
    if not niter is None:
        opts.niter = niter
    if not dst is None:
        check_value(dst, 0, 2)  # Discspec type
        opts.discspec_type = dst
    if not cst is None:
        check_value(cst, 0, 2)  # Contspec type
        opts.contspec_type = cst
    if not nf is None:
        check_value(nf, 0, 1)  # Normflag
        opts.normalization_flag = nf
    if not dis is None:
        check_value(dis, 0, 4)  # Discretization
        opts.discretization = dis
    return opts
