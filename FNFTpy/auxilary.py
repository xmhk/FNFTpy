
def get_lib_path():
    """return the path of the libFNFT file
    This is something you have to edit.
    See example strings.
    """
    libstr = "C:\Libraries\local\libfnft.dll"  # example for windows
    #libstr = "/usr/local/lib/libfnft.so"    #example for linux
    return libstr


def check_value(val, vmin, vmax, vtype=int):
    """raises ValueError when variable has wrong type or is out of range.
    """
    if type(val)!=vtype:
        raise ValueError("Type mismatch expected {}, got {}".format(vtype, type(val)))
    if not( val>=vmin and val <=vmax):
        raise ValueError("Value Error: variable out of range")