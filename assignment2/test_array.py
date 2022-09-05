"""
Tests for our array class
"""

from array_class import Array
import numpy as np


# UNCOMMENT ARRAYS IF USING PYTEST

testarray = Array((3,1), 1,2,3)
other = Array((3,1), 1,2,3)

# 1D tests (Task 4)


def test_str_1d():
    assert str(testarray) == str([1, 2, 3]), "Failed test"


def test_add_1d():
    assert testarray+other == other+testarray == Array((3,1),[2,4,6]), "Failed test"


def test_sub_1d():
    assert testarray-other == other-testarray == Array((3,1),[0,0,0]), "Failed test"


def test_mul_1d():
    assert testarray*other == other*testarray == Array((3,1),[1,4,9]), "Failed test"


def test_eq_1d():
    assert testarray == other and other == testarray, "Failed test"


def test_same_1d():
    assert testarray.is_equal(other) == other.is_equal(testarray) == [True,True,True], "Failed test" 


def test_smallest_1d():
    assert testarray.min_element() == other.min_element() == 1, "Failed test"


def test_mean_1d():
    assert testarray.mean_element() == other.mean_element() == 2, "Failed test"


# 2D tests (Task 6)


def test_add_2d():
    pass


def test_mult_2d():
    pass


def test_same_2d():
    pass


def test_mean_2d():
    pass


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """
    testarray = Array((3,1), 1,2,3)
    other = Array((3,1), 1,2,3)
    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
