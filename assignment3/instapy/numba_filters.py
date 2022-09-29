"""numba-optimized filters"""

from typing import Optional
from numba import njit, prange
import numpy as np

@njit(fastmath=True, parallel=True)
def numba_color2gray(image: np.array, weights: np.array, k: Optional[float]) -> np.array:
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

@njit(fastmath=True, parallel = True)
def numba_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError("k must be between [0-1]")


    sepia_image = np.empty(image.shape)

    max = 0
    for i in prange(image.shape[0]):
        for j in prange(image.shape[1]):
            for l in prange(image.shape[2]):
                val = weights[l][2]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][0]*image[i][j][2]
                
                sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    
    # not parallelized as it causes issues with "max"         
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for l in range(image.shape[2]):
                
                if sepia_image[i][j][l] > max:
                    max = sepia_image[i][j][l]

                sepia_image[i][j][l] = sepia_image[i][j][l]/max*255


    return sepia_image