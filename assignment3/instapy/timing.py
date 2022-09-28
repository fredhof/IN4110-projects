"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import timeit 
import instapy
from . import io
from typing import Callable
import numpy as np
from PIL import Image

from . import python_filters, numpy_filters, numba_filters, cython_filters, importer #imports *.py and cython_filters.so

def time_one(filter_function: Callable, image, weights, calls: int = 3, k: int = 1) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    image_array = np.array(image)
    if ("numba" or "cython") in str(filter_function):
        # numba compiles the function on the first call
        filter_function(image_array, weights)
    if "python" in str(filter_function):
        # python indexes/loops faster with lists than arrays
        image_array= image_array.tolist()
        weights = weights.tolist()
    Image.fromarray(np.uint8(filter_function(image_array, weights, 0.01))).show()
    Image.fromarray(np.uint8(filter_function(image_array, weights, 0.99))).show()
    #return timeit.timeit(lambda: filter_function(image_array, weights), number = calls)/calls # average time

gray_weights = np.array([0.21, 0.72, 0.07])

#a = time_one(python_filters.python_color2gray, importer.rainloc, gray_weights)
#b = time_one(numpy_filters.numpy_color2gray, importer.rainloc, gray_weights)
#c = time_one(numba_filters.numba_color2gray, importer.rainloc, gray_weights)
#d = time_one(cython_filters.cython_color2gray, importer.rainloc, gray_weights)

# NOTE: cython is 30% slower if run after numba compiles, numba is 5% slower if cython runs first
# it adds ~0.0001s to numba (~10% numba, 5% cython)to the time if they are run before python and numpy

#image = np.array(Image.open(importer.rainloc))
#im = numpy_filters.numpy_color2gray(image, gray_weights)
#im = Image.fromarray(np.uint8(im)).show()

#print(c,d)
#print("python", a, '\n', "numpy", b, '\n', "numba", c, "\n", "cython", d)

def make_reports(filename: str = importer.rainloc, calls: int = 5):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = Image.open(filename)
    # print the image name, width, height
    print(f"filename: {image.filename} \nsize(width, heigth): {image.size}\n")
    gray_weights = np.array([0.21, 0.72, 0.07])
    sepia_weights = np.array(([0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]))

    time_one(numpy_filters.numpy_color2sepia, image, sepia_weights, k=0.04)
    l

    # iterate through the filters
    a = "gray"
    filter_names = {f"color2{a}": python_filters.python_color2gray}
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = filter_names[filter_name]
        # time the reference implementation
        reference_time = time_one(reference_filter, image, gray_weights)
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations =  {"numpy": numpy_filters.numpy_color2gray, "numba": numba_filters.numba_color2gray, "cython": cython_filters.cython_color2gray}

        for implementation in implementations:
            filter = implementations[implementation]
            # time the filter
            filter_time = time_one(filter, image, gray_weights)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
