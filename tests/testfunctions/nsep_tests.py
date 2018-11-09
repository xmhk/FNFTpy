import unittest

from .own_test_functions import *
from .external import HiddenPrints
from examples import nsep_example

class Nsep_example(unittest.TestCase):
    def setUp(self):
        with HiddenPrints():
            self.res = nsep_example()

    def test_return_value(self):
        self.assertEqual(self.res['return_value'], 0, "nsep return value not 0")

    def test_M_value(self):
        self.assertEqual(self.res['M'], 7, "M not 7")

    def test_aux_spec_value(self):
        expected = np.array([-0.99999999 - 8.65909474e-01j, -0.99999999 + 8.65909474e-01j,
                         -0.99993896 + 1.87820258e-08j, 0.11814625 + 2.82216353e-07j,
                         0.73222476 + 1.12819764e-08j, 1.29151798 + 6.35545312e-08j,
                         1.82871124 + 8.88012865e-08j])
        self.assertTrue(check_array(
            np.sort_complex(np.around(self.res['aux'], 8)),
            np.sort_complex(expected)
        ), "aux spectrum not as expected")

    def test_K_value(self):
        self.assertEqual(self.res['K'], 11, "K not 11")

    def test_main_spec_value(self):
        expected = np.array([-0.99999999 - 8.65909473e-01j, -0.99999999 - 8.65909475e-01j,
                              -0.99999999 + 8.65909475e-01j, -0.99999999 + 8.65909474e-01j,
                              -0.99999999 - 9.99899604e-01j, -0.99999999 + 9.99899604e-01j,
                              0.1180403 + 6.56652320e-08j, 1.2914677 + 1.11864992e-08j,
                              -0.99977766 - 6.49652790e-06j, 0.73224594 - 1.84219275e-09j,
                              1.8286518 + 1.74944489e-08j])
        self.assertTrue(check_array(
            np.sort_complex(np.around(self.res['main'], 8)),
            np.sort_complex(expected)
        ), "main spectrum not as expected")

    def test_contspec(self):
        expected = {'cont': np.array([
            0.15329981 + 0.12203649j, 0.24385425 + 0.09606438j,
            0.12418466 - 0.00838456j, -0.46324501 + 0.20526334j,
            -0.46324501 - 0.20526334j, 0.12418466 + 0.00838456j,
            0.24385425 - 0.09606438j, 0.15329981 - 0.12203649j])}
        eps = 1e-10

        self.assertTrue(check_array(self.res['cont'],expected['cont']),'contspec as expected')

