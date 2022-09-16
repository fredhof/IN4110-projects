"""pure Python implementation of image filters"""

import numpy as np
from PIL import Image
from itertools import chain
import cProfile

from importer import rainloc
import time
#import sys
#sys.path.append(Arrayloc)
#from array_class import Array

rain = Image.open(rainloc)

def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.asarray(image).tolist()
    # iterate through the pixels, and apply the grayscale transform
    weights = [0.21, 0.72, 0.07]
    tid = time.time()
    dims = len(gray_image), len(gray_image[0]), len(gray_image[:][0][0])
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                gray_image[i][j][k] *= weights[k]
            gray_image[i][j] = sum(gray_image[i][j])
    print(time.time()-tid)
    gray_image = Image.fromarray(np.uint8(gray_image))
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
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


python_color2gray(rain)