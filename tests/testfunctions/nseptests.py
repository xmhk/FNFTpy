from .fnftpy_testutils import Richtigbenennen
import numpy as np

def nsep_example_test(res):
    infostr = "nsep (resemble C example)"
    tmp = Richtigbenennen(infostr=infostr)
    expected = {
        'K': 11,
        'main': np.array([-0.99999999 - 8.65909473e-01j, -0.99999999 - 8.65909475e-01j,
                          -0.99999999 + 8.65909475e-01j, -0.99999999 + 8.65909474e-01j,
                          -0.99999999 - 9.99899604e-01j, -0.99999999 + 9.99899604e-01j,
                          0.1180403 + 6.56652320e-08j, 1.2914677 + 1.11864992e-08j,
                          -0.99977766 - 6.49652790e-06j, 0.73224594 - 1.84219275e-09j,
                          1.8286518 + 1.74944489e-08j]),
        'M': 7,
        'aux': np.array([-0.99999999 - 8.65909474e-01j, -0.99999999 + 8.65909474e-01j,
                         -0.99993896 + 1.87820258e-08j, 0.11814625 + 2.82216353e-07j,
                         0.73222476 + 1.12819764e-08j, 1.29151798 + 6.35545312e-08j,
                         1.82871124 + 8.88012865e-08j])}
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_value, res['K'], 11, "K")
    tmp.single_test(tmp.check_value, res['M'], 7, "M")
    # as the order of spectra is not clear, we round to 8 digits, sort and compare
    # to sample data
    tmp.single_test(tmp.check_array,
                     np.sort_complex(np.around(res['main'], 8)),
                     np.sort_complex(expected['main']), "main spectrum")
    tmp.single_test(tmp.check_array,
                     np.sort_complex(np.around(res['aux'], 8)),
                     np.sort_complex(expected['aux']), "auxiliary spectrum")
    return tmp
