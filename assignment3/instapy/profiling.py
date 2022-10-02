"""
Profiling (IN4110 only)
"""

import pstats
import cProfile
import line_profiler

import numpy as np

import instapy
from instapy import io


def profile_with_cprofile(filter, image_array, weights, k, ncalls=5):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (np.array): image to filter
        ncalls (int): number of repetitions to measure
    """
    profiler = cProfile.Profile()

    # same as: profiler.runcall(filter, image_array, weights, k)
    profiler.enable()
    for i in range(ncalls): filter(image_array, weights, k)
    profiler.disable()

    # print the top 10 results, sorted by cumulative time
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(10)


def profile_with_line_profiler(filter, image_array, weights, k, ncalls=5):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    # create the LineProfiler
    profiler = line_profiler.LineProfiler()
    # tell it to measure the function we are given
    profiler.add_function(filter)
    # Measure filter(image)
    for i in range(ncalls): profiler.runcall(filter, image_array, weights, k)
    # print statistics
    profiler.print_stats()

def run_profiles(profiler: str = "cprofile"):
    """Run profiles of every implementation

    Args:

        profiler (str): either 'line_profiler' or 'cprofile'
    """
    # Select which profile function to use
    if profiler == "line_profiler":
        profile_func = profile_with_line_profiler
    elif profiler.lower() == "cprofile":
        profile_func = profile_with_cprofile
    else:
        raise ValueError(f"{profiler=} must be 'line_profiler' or 'cprofile'")

    # construct a random 640x480 image
    image_array = io.random_image(640,480)

    gw = np.array([0.21, 0.72, 0.07])
    sw = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
    k = 1

    filter_names = ["color2gray", "color2sepia"]
    implementations = ["python", "numpy", "numba", "cython"]
    for filter_name in filter_names:
        for implementation in implementations:
            print(f"Profiling {implementation} {filter_name} with {profiler}:")
            filter = instapy.get_filter(filter_name, implementation)  #
            
            if "gray" in filter_name: weights = gw
            if "sepia" in filter_name: weights = sw

            # call it once (compiles numba)
            filter(image_array, weights, k)
            profile_func(filter, image_array, weights, k)


if __name__ == "__main__":
    print("Begin cProfile")
    run_profiles("cprofile")
    print("End cProfile")
    print("Begin line_profiler")
    run_profiles("line_profiler")
    print("End line_profiler")
