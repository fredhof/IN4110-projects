"""numpy implementation of image filters"""
from typing import Optional
import numpy as np

def numpy_color2gray(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array): the original image array
        weights (np.array): the weights of the transformation
        k (float): amount of filter to apply (optional)
    Returns:
        np.array: gray_image, the transformed image
    """
    # vectorized implementation of gray pure Python filter, slower than np.matmul.
    # image[:,:,0]*weights[0] + image[:,:,1]*weights[1] + image[:,:,2]*weights[2] # identical to np.dot(image, weights)
    
    return image @ weights #matrix multiplication using np.matmul

def numpy_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
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
        raise ValueError(f"k must be between [0-1], got {k=}")
    # vectorized implementation of the sepia transform
    image = image * (1-k) + image @ weights.T * k

    return image/np.max(image)*255