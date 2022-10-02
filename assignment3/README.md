# instapy
instapy is an image processing module that can transform a image using the grayscale or sepia transforms, scale/resize it, display and save to file.\
For sepia transformations it supports scaling by a constant k = [0,1], where k=0 returns the original image and k=1 returns the sepia transformed image.\
instapy supports four different implementations for the gray and sepia filters: pure Python, NumPy, Numba, Cython. It can also track the run time of the given implementation.

### Installation instructions
Clone the repository, "cd" into it and install with pip as `pip install .`. The command may differ depending on your system. \
Then you have to compile the Cython file. That can be done as `python3 setup.py build_ext -i`.

### Usage
The package can be run as `python3 -m instapy *args **kwargs`.\
Running `python3 -m instapy -h` will display the instruction manual.\
```
positional arguments:
  file                  The filename to apply filter to

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     The output filename
  -g, --gray            Transform with the gray filter
  -se, --sepia          Transform with the sepia filter
  -k K, --k K           The scaling of the transformation. k=0 gives the original image, k=1 (default) gives the transformed image. Currently only supports sepia scaling.
  -sc SCALE, --scale SCALE
                        Uniformly scale the size of the image by a constant
  -i IMPLEMENTATION, --implementation IMPLEMENTATION
                        Specify implementation. Supports: python, numpy, numba, cython.
  -r, [RUNTIME], --runtime [RUNTIME]
                        Tracks the average run time with timeit.timeit. Specify number of runs, default is 5.

```
