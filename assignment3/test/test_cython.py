from instapy.cython_filters import cython_color2gray, cython_color2sepia

import numpy.testing as nt

def test_color2gray(image, gray_weights, reference_gray):
    image = cython_color2gray(image, gray_weights)
    nt.assert_allclose(image, reference_gray)


def test_color2sepia(image, sepia_weights, reference_sepia):
    image = cython_color2sepia(image, sepia_weights)
    nt.assert_allclose(image, reference_sepia)
