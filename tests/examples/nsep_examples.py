from FNFTpy import nsep
import numpy as np

def nsep_example():
    print("\n\nnsep example")
    # set values
    D = 256
    dt = 2 * np.pi / D
    tvec = np.arange(D) * dt
    q = np.exp(2.0j * tvec)
    # call function
    res = nsep(q, 0, 2 * np.pi, bb=[-2, 2, -2, 2], filt=1)
    # print results
    print("\n----- options used ----")
    print(res['options'])
    print("\n------ results --------")
    print("FNFT return value: %d (should be 0)" % res['return_value'])
    print("number of samples: %d" % D)
    print('main spectrum')
    for i in range(res['K']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['main'][i]),
                                          np.imag(res['main'][i])))
    print('auxiliary spectrum')
    for i in range(res['M']):
        print("%d :  %.6f  %.6fj" % (i, np.real(res['aux'][i]),
                                          np.imag(res['aux'][i])))
    return res