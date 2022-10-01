from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.numba_filters import numba_color2gray, numba_color2sepia

import numpy.testing as nt
import numpy as np
from PIL import Image
from instapy import importer

def test_color2gray(image, gray_weights, reference_gray):
    image = numpy_color2gray(image, gray_weights)
    nt.assert_allclose(image, reference_gray)


def test_color2sepia(image, sepia_weights, reference_sepia):
    image = numpy_color2sepia(image, sepia_weights)
    nt.assert_allclose(image, reference_sepia)

im = np.asarray(Image.open(importer.rainloc))


w = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
s = numpy_color2sepia(im, w)
ref = python_color2sepia(im, w)

b = numba_color2sepia(im, w)
Image.fromarray(np.uint8(s)).save('b.png')
Image.fromarray(np.uint8(ref)).save('a.png')
Image.fromarray(np.uint8(b)).save('c.png')
#test_color2sepia(im, w, ref)

o = np.empty(im.shape)
for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        for l in range(im.shape[2]):
            o[i][j][l] = w[l][2]*im[i][j][0] + w[l][1]*im[i][j][1] + w[l][0]*im[i][j][2]

print(o, (im @ w).T)