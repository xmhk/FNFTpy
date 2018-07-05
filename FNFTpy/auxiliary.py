def get_lib_path():
    """Return the path of the FNFT file.


    Here you can set the location of the compiled library for FNFT.
    See example strings below.
    """
    libstr = "C:/Libraries/local/libfnft.dll"  # example for windows
    # libstr = "/usr/local/lib/libfnft.so"  # example for linux
    return libstr


def check_value(val, vmin, vmax, vtype=int):
    """Raise and ValueError when variable has wrong type or is out of range.

        Arguments:

            val : variable to check
            vmin : minimum value val should take
            vmax : maximum value val should take

        optional Arguments:

            vtype : type val should take
    """
    if type(val) != vtype:
        raise ValueError("Type mismatch expected {}, got {}".format(vtype, type(val)))
    if not (vmin <= val <= vmax):
        raise ValueError("Value Error: variable out of range")
