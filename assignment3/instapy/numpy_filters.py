"""numpy implementation of image filters"""
from typing import Optional
import numpy as np

def numpy_color2gray(image: np.array, weights: np.array, k: Optional[float]) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    # np.round(np.dot(image,weights),10) == np.round(image @ weights,10), dif
    # image[:,:,0]*weights[0] + image[:,:,1]*weights[1] + image[:,:,2]*weights[2] # identical to np.dot(image, weights)
    return image @ weights #matrix multiplication using np.matmul

def numpy_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    image = image * (1-k) + image @ weights.T * k

    return image/np.max(image)*255