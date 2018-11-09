import numpy as np

def check_array(value, expectedval, eps=1e-10):
    """Test array == expectedarray  (norm < eps)"""
    return np.sum(np.abs(value - expectedval) ** 2) < eps

def check_boolarray(value, expectedval):
        """Test boolean array == expected"""
        return (value == expectedval).all()