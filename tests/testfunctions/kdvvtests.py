from .richtigbenennen import Richtigbenennen
import numpy as np

def kdvv_example_test(res):
    tmp = Richtigbenennen()
    #tmp.infostr = "Mimic kdvv C example."
    expected = {'cont': np.array([
        0.15329981+0.12203649j,  0.24385425+0.09606438j,
        0.12418466-0.00838456j, -0.46324501+0.20526334j,
        -0.46324501-0.20526334j,  0.12418466+0.00838456j,
        0.24385425-0.09606438j,  0.15329981-0.12203649j])}
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_array, res['cont'], expected['cont'], "continuous spectrum")
    return tmp