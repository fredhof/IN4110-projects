"""Cython implementation of filter functions"""

from typing import Optional
from PIL import Image
import numpy as np

cimport numpy as np
cimport cython
#from cython.parallel import prange # import if parallelizing, having issues so not parallelized
np.import_array()

DTYPE = np.double

# cython declarations that speed things up
@cython.cdivision(True) # enables C-division
@cython.nonecheck(False) # disables all checks
@cython.boundscheck(False) # disable out of bounds check
@cython.wraparound(False) # disables [-1, -2, ..] etc.
# function types declared "const" as they are constant (speed/safety reasons)
def cython_color2gray(const np.npy_uint8[:,:,::1] image, const double[::1] weights, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array): the original image array
        weights (np.array): the weights of the transformation
        k (float): amount of filter to apply (optional)
    Returns:
        np.array: gray_image, the transformed image
    """
    
    # creates native c index/loop variable
    cdef size_t H = image.shape[0]
    cdef size_t W = image.shape[1]

    # C contiguous [::1] (numpy like) memoryviews [:,:] (cython vectorized array)
    # for more info: https://docs.cython.org/en/latest/src/userguide/numpy_tutorial.html
    g = np.empty((H,W), dtype=DTYPE)
    cdef double[:,::1] gray_image = g 

    cdef size_t i, j
    for i in range(H):
        for j in range(W):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image


# cython declarations that speed things up
@cython.cdivision(True) # enables C-division
@cython.nonecheck(False) # disables all checks
@cython.boundscheck(False) # disable out of bounds check
@cython.wraparound(False) # disables [-1, -2, ..] etc.
# function types declared "const" as they are constant (speed/safety reasons)
def cython_color2sepia(const np.npy_uint8[:,:,::1] image, const double[:,::1] weights, const double k = 1) -> np.array:
    """Convert rgb pixel array to sepia
    
    Args:
        image (np.array): the original image array
        weights (np.array): the weights of the transformation
        k (float): amount of filter to apply (optional)
    Returns:
        np.array: sepia_image, the transformed image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError("k must be between [0-1]")
    
    # creates native c index/loop variable
    cdef size_t H = image.shape[0]
    cdef size_t W = image.shape[1]
    cdef size_t D = image.shape[2]

    # C contiguous [::1] (numpy like) memoryviews [:,:] (cython vectorized array)
    # for more info: https://docs.cython.org/en/latest/src/userguide/numpy_tutorial.html
    s = np.empty((H,W,D), dtype=DTYPE)
    cdef double[:,:,::1] sepia_image = s 

    cdef size_t i, j, l
    cdef double val, maxx
    
    # iterate through the pixels, and apply the sepia transform
    for i in range(H):
        for j in range(W):
            for l in range(D):
                val = weights[l][2]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][0]*image[i][j][2]

                sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    
                if sepia_image[i][j][l] > maxx:
                    maxx = sepia_image[i][j][l] 
                    
    # new looop now that max is properly defined
    for i in range(H):
        for j in range(W):
            for l in range(D):
                sepia_image[i][j][l] = sepia_image[i][j][l]/maxx*255

    return sepia_image

