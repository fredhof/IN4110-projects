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

def time_one(filter_function: Callable, image, weights, k: float = 1., calls: int = 5) -> float:
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
    if "numba" in str(filter_function):
        # numba compiles the function on the first call
        filter_function(image_array, weights, k)

    if "python" in str(filter_function):
        # python indexes/loops faster with lists than arrays
        image_array= image_array.tolist()
        weights = weights.tolist()

    return timeit.timeit(lambda: filter_function(image_array, weights, k), number = calls)/calls # average time


def make_reports(filename: str = importer.rainloc, calls: int = 5):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = Image.open(filename)
    gray_weights = np.array([0.21, 0.72, 0.07])
    sepia_weights = np.array(([0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]))

    filter_colors = ["color2gray", "color2sepia"]  
    weights = [gray_weights, sepia_weights]
    writing_file = "timing-report.txt"
    
    print(f"Writing performance report (timed with timeit.timeit) to {writing_file}...")
    
    with open(writing_file, "w") as file:
        
        file.write(f"Timing performed using timeit.timeit with file: {image.filename} \ndimensions(width, heigth): {image.size}\n")
        file.write("-"*100); file.write("\n"*2)
        for color in range(len(filter_colors)):
            
            filter_names = {f"{filter_colors[color]}": [python_filters.python_color2gray, python_filters.python_color2sepia]}
            for filter_name in filter_names:
                
                # get the reference filter function
                reference_filter = filter_names[filter_name]
                
                # time the reference implementation
                reference_time = time_one(reference_filter[color], image, weights[color], calls = calls)
                file.write(f"Reference (pure Python) filter average time ({calls=}) {filter_name}: {reference_time:.3e}s \n")
                
                # iterate through the implementations
                implementations =  {"numpy": [numpy_filters.numpy_color2gray, numpy_filters.numpy_color2sepia],\
                "cython": [cython_filters.cython_color2gray, cython_filters.cython_color2sepia],\
                "numba": [numba_filters.numba_color2gray, numba_filters.numba_color2sepia]}

                for implementation in implementations:
                    
                    filter = implementations[implementation]
                    # time the filter
                    filter_time = time_one(filter[color], image, weights[color], calls = calls)
                    
                    # compare the reference time to the optimized time
                    speedup = reference_time/filter_time
                    file.write(f"{implementation} {filter_name}: {filter_time:.3e}s ({speedup=:.2f}x)\n")
            
            file.write("\n")
        print("Done.")


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports(calls = 10)
