from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt

def test_color2gray(image, gray_weights, reference_gray):
    image = numpy_color2gray(image, gray_weights)
    nt.assert_allclose(image, reference_gray)


def test_color2sepia(image, sepia_weights, reference_sepia):
    image = numpy_color2sepia(image, sepia_weights)
    nt.assert_allclose(image, reference_sepia)