"""
Array class for assignment 2
"""


import re


class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,)..
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        # This allowes us to input lists/tuples aswell, so that Array(shape, [1,2,3]) == Array(shape, 1,2,3)
        if len(values) == 1 and isinstance(values,tuple):
            values = values[0]

        if not isinstance(shape, tuple) or not all(isinstance(x, (int, float, bool)) for x in values):
            raise TypeError(f"Ensure that the shape is of type {tuple} and/or that the values are of a valid type.")
       
        if not all(isinstance(x, type(values[0])) for x in values[1:]):
            raise ValueError("The values of are not all of the same type.")

        from math import prod # import product summation from Pythons math library
        if prod(shape) != len(values):
            raise ValueError(f"The number of values: {len(values)}, do not fit the shape of the array: {shape}.")


        self.shape = shape
        self.array = [*values]
        self.values = [*values]
        

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        Example:
        [0,1], [2,3] -> [0,1]
                        [2,3]

        """
        arr = self._reshape(self.values)


        return str(arr).replace('],', ']\n')
        


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        # check that the method supports the given arguments (check for data type and shape of array)


        if isinstance(other,(int,float)):
            return Array(self.shape, [self.array[i] + other for i in range(len(self.array))])

        if isinstance(self.array,bool) or isinstance(other,bool):
            return NotImplemented

        assert len(self.array) == len(other.array), "Arrays do not have the same dimensions."
               
        return Array(self.shape, [self.array[i] + other.array[i] for i in range(len(self.array))])

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        return self.__add__(-other)

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        
        return -self.__sub__(other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if isinstance(other,(int,float)):
            return Array(self.shape, [self.array[i] * other for i in range(len(self.array))])

        if isinstance(self.array,bool) or isinstance(other,bool):
            return NotImplemented

        assert len(self.array) == len(other.array), "Arrays do not have the same dimensions."
        
        return Array(self.shape, [self.array[i] * other.array[i] for i in range(len(self.array))])

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        return self.array == other.array

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if isinstance(other,(int,float)):
            return [self.array[i] == other for i in range(len(self.array))]

        
        return [self.array[i] == other.array[i] for i in range(len(self.array))]

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        return min(self.array)

    def max_element(self):
        return max(self.array)

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """

        return sum(self.array)/len(self.array)

    def _reshape(self,vals):
        
        # Example reshaping
        # zero = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # zero = [[0 0], [0 0], [0 0], [0 0], [0 0], [0 0]]
        # zero = [ [[0 0] [0 0]], [[0 0] [0 0]], [[0 0] [0 0]]]
        
        for i in range(1, len(self.shape)):
            
            arr1 = []
            point = len(vals) // self.shape[-i]
            

            for j in range(point):
                arr2 = []

                for k in range(self.shape[-i]):
                    arr2.append(vals[k + j*self.shape[-i]])
                
                arr1.append(arr2)
            vals = arr1

        return vals


    def __getitem__(self, item):
        return self._reshape(self.values)[item]
        
    def __len__(self, arr):
        return len(arr)

    def __neg__(self):
        return Array(self.shape, [-x for x in self.array])

if __name__ == '__main__':
    
    myarray2 = Array((3,3), *range(3*3)) # = Array = [(3,3), 0,1,..,8]
    myarray3 = Array((3,3,2), *range(3*3*2))
    myarrayX = Array((3,6,1,7,9), *range(3*6*1*7*9))

    print(2-myarray3)