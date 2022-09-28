"""pure Python implementation of image filters"""

import numpy as np

def python_color2gray(image: list, weights: list) -> list:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    
    # iterate through the pixels, and apply the grayscale transform
    gray_image = np.empty((len(image), len(image[0])))

    for i in range(gray_image.shape[0]):
        for j in range(gray_image.shape[1]):
            gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    
    return gray_image


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
