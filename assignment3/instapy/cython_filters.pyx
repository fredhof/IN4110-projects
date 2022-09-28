"""Cython implementation of filter functions"""

from PIL import Image
import numpy as np

cimport numpy as np
cimport cython
from cython.parallel import prange
np.import_array()

@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
def cython_color2gray(np.npy_uint8[:,:,::1] image, double[::1] weights):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    DTYPE = np.single
        
    cdef size_t H = image.shape[0]
    cdef size_t W = image.shape[1]

    g = np.empty((H,W), dtype=DTYPE)
    cdef float[:,::1] gray_image = g 

    cdef size_t i, j
    for i in prange(H,nogil=True):
        for j in prange(W):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image


    #return image @ weights #matrix multiplication using np.matmul


