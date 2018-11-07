from .richtigbenennen import Richtigbenennen
import numpy as np


def nsev_inverse_example_test(res):
    infostr = "Mimic nsev_inverse C example."
    tmp = Richtigbenennen()
    expected = {
        'qsamprange':[0,-1,40],
        'qsamp':
           np.array([-8.51156134e-07-2.59723802e-03j,-8.51152031e-07-5.05389982e-03j,
                    -8.51152828e-07-9.77009846e-03j, -8.51153739e-07-1.88124421e-02j,
                    -8.51154704e-07-3.61352219e-02j, -8.51155662e-07-6.93026882e-02j,
                     -8.51156430e-07-1.32772848e-01j, -8.51156724e-07-2.54100125e-01j,
                     -8.51156012e-07-4.85242920e-01j, -8.51152998e-07-9.20351895e-01j,
                     -8.51144440e-07-1.70480071e+00j, -8.51123774e-07-2.91920894e+00j,
                     -8.51093260e-07-4.03290079e+00j, -8.51159989e-07-2.42570391e-03j,
                     -8.51157880e-07-5.62308393e-04j, -8.51156117e-07-4.40370675e-04j,
                     -8.51154654e-07-3.63745902e-04j, -8.51153407e-07-3.03868218e-04j,
                     -8.51152359e-07-2.54859627e-04j, -8.51151499e-07-2.14146911e-04j,
                     -8.51150765e-07-1.80118348e-04j, -8.51150137e-07-1.51591858e-04j,
                     -8.51149618e-07-1.27638782e-04j, -8.51149196e-07-1.07506128e-04j,
                     -8.51148829e-07-9.05737153e-05j, -8.51148517e-07-7.63264783e-05j]),
        'Xi':np.array([-401.33884499, 401.73116058])
                   }
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_array,
                     res['q'][expected['qsamprange'][0]:expected['qsamprange'][1]:expected['qsamprange'][2]],
                     expected['qsamp'],"q values")
    tmp.single_test(tmp.check_array, res['Xi'], expected['Xi'], 'Xi')
    return tmp

def nsev_inverse_example2_test(res):
    infostr = "nsev_inverse_example: create a N=2.2 Satsuma-Yajima pulse."
    tmp = Richtigbenennen()
    expected = {
        'qsamprange': [0, -1, 40],
        'qsamp': np.array(
            [1.34230102e-06 - 5.04465255e-15j, 4.34817385e-06 - 6.31865362e-15j,
             1.40574450e-05 - 3.14973971e-15j, 4.54326063e-05 - 2.19330861e-15j,
             1.46827533e-04 - 1.55620563e-15j, 4.74508381e-04 - 2.66429125e-16j,
             1.53348456e-03 + 2.32701341e-16j, 4.95580127e-03 + 2.84806416e-16j,
             1.60155854e-02 + 3.90817711e-16j, 5.17513079e-02 + 1.71484418e-15j,
             1.67026494e-01 + 4.65750576e-15j, 5.32522012e-01 + 7.39474890e-15j,
             1.50907411e+00 + 3.81190249e-15j, 2.13338526e+00 + 5.18397891e-15j,
             1.00280857e+00 + 6.77405341e-15j, 3.26530063e-01 + 4.90563790e-15j,
             1.01548385e-01 + 1.62058722e-15j, 3.14376794e-02 + 1.95891048e-16j,
             9.72830255e-03 + 2.30171230e-16j, 3.01026309e-03 + 5.24089935e-16j,
             9.31471124e-04 + 4.39924210e-16j, 2.88226276e-04 - 6.56173293e-16j,
             8.91859214e-05 - 1.96145018e-15j, 2.75963271e-05 - 2.67063774e-15j,
             8.53801078e-06 - 4.81025786e-15j, 2.63963808e-06 - 7.13301617e-15j]
        )}
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_array,
                     res['q'][
                     expected['qsamprange'][0]:expected['qsamprange'][1]:expected['qsamprange'][2]],
                     expected['qsamp'], "q values")
    return tmp
