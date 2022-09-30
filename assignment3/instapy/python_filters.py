"""pure Python implementation of image filters"""

from typing import Optional
import numpy as np

def python_color2gray(image: list, weights: list, k: Optional[float]) -> list:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    
    # iterate through the pixels, and apply the grayscale transform
    gray_image = np.empty((len(image), len(image[0]))).tolist()

    for i in range(len(gray_image)):
        for j in range(len(gray_image[0])):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image


def python_color2sepia(image: list, weights: list, k: Optional[float] = 1) -> list:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty((len(image), len(image[0]), len(image[0][0]))).tolist()
    max = 0
    for i in range(len(sepia_image)):
        for j in range(len(sepia_image[0])):
            for l in range(len(sepia_image[0][0])):
                val = (weights[l][2]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][0]*image[i][j][2]) 

                sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
                
                if sepia_image[i][j][l] > max:
                    max = sepia_image[i][j][l]

    for i in range(len(sepia_image)):
        for j in range(len(sepia_image[0])):
            for l in range(len(sepia_image[0][0])):
                sepia_image[i][j][l] = sepia_image[i][j][l]/max*255


    return sepia_image