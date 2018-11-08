from .fnftpy_testutils import Richtigbenennen
#from tests.testfunctions.fnftpy_testutils.richtigbenennen import Richtigbenennen
import numpy as np
from FNFTpy import nsev

def nsev_example_test(res):
    infostr = "nsev example (resemble C example)"
    tmp = Richtigbenennen(infostr=infostr)
    expected = {'bound_states_num': 1,
                'bound_states': np.array([2.13821177e-50 + 1.57422601j]),
                'disc_norm': np.array([-1. - 2.56747175e-50j]),
                'cont_ref': np.array([
                    -0.10538565 - 0.42577137j, -0.78378026 - 1.04297186j,
                    -1.09090439 - 1.33957378j, -1.16918546 - 0.48325228j,
                    -1.16918546 + 0.48325228j, -1.09090439 + 1.33957378j,
                    -0.78378026 + 1.04297186j, -0.10538565 + 0.42577137j]),
                }
    tmp.single_test(tmp.check_value, res['return_value'], 0, "FNFT return value")
    tmp.single_test(tmp.check_value, res['bound_states_num'], 1, "number of bound states")
    tmp.single_test(tmp.check_array, res['bound_states'], expected['bound_states'], "bound states")
    tmp.single_test(tmp.check_array, res['disc_norm'], expected['disc_norm'], "norming consts")
    tmp.single_test(tmp.check_array, res['cont_ref'], expected['cont_ref'], "cont. reflection coeff.")
    return tmp


def nsev_dstcst_variation():
    # set values
    D = 256
    tvec = np.linspace(-1, 1, D)
    q = np.zeros(len(tvec), dtype=np.complex128)
    q[:] = 2.3 / np.cosh(tvec)
    res = {}
    # different switches for discrete spectrum type
    for dst in [-1, 0, 1, 2, 3]:
        tmpres = nsev(q, tvec, dst=dst, )
        res['dst=%d' % dst] = np.array([tmpres['return_value'] == 0,
                                             'disc_res' in tmpres.keys(),
                                             'disc_norm' in tmpres.keys()])
    # different switches for continuous spectrum type
    for cst in [-1, 0, 1, 2, 3]:
        tmpres = nsev(q, tvec, cst=cst, )
        res['cst=%d' % cst] = np.array([
            tmpres['return_value'] == 0,
            'cont_ref' in tmpres.keys(),
            'cont_a' in tmpres.keys(),
            'cont_b' in tmpres.keys()])
    # calulate neither discrete nor continuous spectrum
    tmpres = nsev(q, tvec, dst=3, cst=3)
    res['dst=3cst=3'] = np.array([tmpres['return_value'] == 0,
                                       'disc_res' in tmpres.keys(),
                                       'disc_norm' in tmpres.keys(),
                                       'cont_ref' in tmpres.keys(),
                                       'cont_a' in tmpres.keys(),
                                       'cont_b' in tmpres.keys()
                                       ])
    return res


def nsev_dstcst_variation_test(res):
    infostr="nsev: checks for dst and cst switches"
    tmp = Richtigbenennen(infostr=infostr)
    expected = {'dst=-1': np.array([ True, False, False]),
                'dst=0': np.array([ True, False,  True]),
                'dst=1': np.array([ True,  True, False]),
                'dst=2': np.array([ True,  True,  True]),
                'dst=3': np.array([ True, False, False]),
                'cst=-1': np.array([ True, False, False, False]),
                'cst=0': np.array([ True,  True, False, False]),
                'cst=1': np.array([ True, False,  True,  True]),
                'cst=2': np.array([ True,  True,  True,  True]),
                'cst=3': np.array([ True, False, False, False]),
                'dst=3cst=3': np.array([ True, False, False, False, False, False])}
    for k in expected.keys():
        tmp.single_test(tmp.check_boolarray, res[k], expected[k], "check option: %s"%k)
    return tmp