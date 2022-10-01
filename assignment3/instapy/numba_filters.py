"""numba-optimized filters"""

from typing import Optional
from numba import njit, prange
import numpy as np

@njit(fastmath=True, parallel=True)
def numba_color2gray(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array): the original image array
        weights (np.array): the weights of the transformation
        k (float): amount of filter to apply (optional)
    Returns:
        np.array: gray_image, the transformed image
    """
    
    #initialize empty filtered array to assigne values to
    #reduce RGB to grayscale (y,x,3) -> (y,x) as they are uniform, massive speedup
    gray_image = np.empty(image.shape[0:2]) 

    # same as: np.dot(image, weights)
    for i in prange(image.shape[0]):
        for j in prange(image.shape[1]):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image

@njit(fastmath=True, parallel = True)
def numba_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
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

    #initialize empty filtered array to assigne values to
    sepia_image = np.empty(image.shape)

    # weights needs to be transposed for summation to work nicely
    # same as: image * (1-k) + np.dot(image, weights.T) * k, if k=0 it reduces to image, if k=1 it reduces to np.dot(image, weights.T)
    for i in prange(image.shape[0]):
        for j in prange(image.shape[1]):
            for l in prange(image.shape[2]):
                val = weights[l][2]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][0]*image[i][j][2]
                
                sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    
    # not parallelized since it will cause issues.
    maxx = 0  
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for l in range(image.shape[2]):
                if sepia_image[i][j][l] > maxx:
                    maxx = sepia_image[i][j][l] 

    # normalizes the array so it can be transformed to uint8 without loss
    for i in prange(image.shape[0]):
        for j in prange(image.shape[1]):
            for l in prange(image.shape[2]):     
                sepia_image[i][j][l] = sepia_image[i][j][l]/maxx*255


    return sepia_image