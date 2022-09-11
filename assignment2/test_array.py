"""
Tests for our array class
"""

from array_class import Array

testarray1d = Array((3,1), 1,2,3)
otherarray1d = Array((3,1), 1,2,3)

testarray2d = Array((3,2), 1,2,3,4,5,6)
otherarray2d = Array((3,2), 1,2,3,4,5,6)
print(testarray2d)

num = 2

# 1D tests (Task 4)
def test_str_1d():
    assert print(testarray1d) == print(otherarray1d) == print([1, 2, 3]), "Failed test" #will print the statements

def test_add_1d():
    assert testarray1d+otherarray1d == otherarray1d+testarray1d == Array((3,1),[2,4,6]), "Failed test"
    assert testarray1d+num == otherarray1d+num == num+testarray1d == num+otherarray1d == Array((3,1), [3,4,5]), "Failed test"

def test_sub_1d():
    assert testarray1d-otherarray1d == otherarray1d-testarray1d == Array((3,1),[0,0,0]), "Failed test"
    assert testarray1d-num == otherarray1d-num == Array((3,1), [-1,0,1]) != num-testarray1d == num-otherarray1d, "Failed test"
    assert num-testarray1d == num-otherarray1d == Array((3,1), [1,0,-1]) != testarray1d-num == otherarray1d-num, "Failed test"


def test_mul_1d():
    assert testarray1d*otherarray1d == otherarray1d*testarray1d == Array((3,1),[1,4,9]), "Failed test"
    assert testarray1d*num == otherarray1d*num == num*testarray1d == num*otherarray1d == Array((3,1), [2,4,6]), "Failed test"

def test_eq_1d():
    assert testarray1d == otherarray1d and otherarray1d == testarray1d, "Failed test"


def test_same_1d():
    assert testarray1d.is_equal(otherarray1d) == otherarray1d.is_equal(testarray1d) == [True,True,True], "Failed test" 


def test_smallest_1d():
    assert testarray1d.min_element() == otherarray1d.min_element() == 1, "Failed test"


def test_mean_1d():
    assert testarray1d.mean_element() == otherarray1d.mean_element() == 2, "Failed test"


# 2D tests (Task 6)


def test_add_2d():
    assert testarray1d+otherarray1d == otherarray1d+testarray1d == Array((3,2),[2,4,6,8,10,12]), "Failed test"
    assert testarray1d+num == otherarray1d+num == num+testarray1d == num+otherarray1d == Array((3,2),[2,4,6,8,10,12]), "Failed test"


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
    #testarray1d = Array((3,1), 1,2,3)
    #otherarray1d = Array((3,1), 1,2,3)
    #num = 2
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
