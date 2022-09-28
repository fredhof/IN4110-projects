"""numba-optimized filters"""
from numba import njit, prange
import numpy as np

@njit(fastmath=True, parallel=True)
def numba_color2gray(image: np.array, weights: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    
    # iterate through the pixels, and apply the grayscale transform
    gray_image = np.empty(image.shape[0:2]) # reduce RGB to grayscale (y,x,3) -> (y,x), massive speedup

    for i in prange(image.shape[0]):
        for j in prange(image.shape[1]):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image

@njit(fastmath=True, parallel=True)
def python_color2sepia(image: list) -> list:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    ...

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image