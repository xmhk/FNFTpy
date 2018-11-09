import unittest

from .own_test_functions import *
from .external import HiddenPrints
from examples import kdvv_example

class Kdvv_example(unittest.TestCase):
    def setUp(self):
        with HiddenPrints():
            self.res = kdvv_example()

    def test_return_value(self):
        self.assertEqual(self.res['return_value'], 0, "kdvv return value")
    def test_contspec(self):
        expected = {'cont': np.array([
            0.15329981 + 0.12203649j, 0.24385425 + 0.09606438j,
            0.12418466 - 0.00838456j, -0.46324501 + 0.20526334j,
            -0.46324501 - 0.20526334j, 0.12418466 + 0.00838456j,
            0.24385425 - 0.09606438j, 0.15329981 - 0.12203649j])}
        eps = 1e-10

        self.assertTrue(check_array(self.res['cont'],expected['cont']),'contspec as expected')