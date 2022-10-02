# Profiling report

## Questions

A few questions below to help understand the kind of information we can get from profiling outputs.
 We are not asking for lots of detail, just 1-2 sentences each.

### Question 1

> Which profiler produced the most useful output, and why?

cProfile gives the most accurate results, but is not formated "nicely", however it gives deeper function calls (see cProfile numpy_color2sepia).
line-profiler gives a nicely formatted output.
So I guess the answer depends on what you want. cProfile for more detailed output, or line_profiler for a nicer visualization.
line_profiler is probably better to if you are struggeling to understand the bottlenecks of your code, but if you are a pro cProfile is the way to go.

Neither cProfile or line_profiler works (properly) with Numba or Cython as it is compiled code.
A more proper, indepth answer regarding Numba and Cython is given at [StackOverflow](https://stackoverflow.com/questions/54545511/using-line-profiler-with-numba-jitted-functions).

### Question 2

> Pick one profiler output (e.g. `cprofile numpy_color2sepia`).
  Based on this profile, where should we focus effort on improving performance?

> **Hint:** two things to consider when picking an optimization:

> - how much time is spent in the step? (reducing a step that takes 1% of the time all the way to 0 can only improve performance by 1%)
> - are there other ways to do it? (simple steps may already be optimal. Complex steps often have many implementations with different performance)

selected profile: line_profiler python_color2sepia

I chose python_color2sepia as it was the longest code and line_profiler since it gives the most detailed output.
80% of the time is spent in the first for loop segment. The most time goes to assigning values to val and sepia_image.
One could think that removing val and insertinging it into sepia_image would make it run faster, but that is false as item assignments are executed in Python and reused.
It would also make it less readable.
Three ways I see to improve performance is to parellelize the code with the multiprocessing module, vectorize the code (numpy), used compiled, vectorized code (numba, cython). 

I omitted numpy as it is already vectorized, and numba and cython as they provide compiled code and will give skewed results.
Note the weird output in cython_color2sepia, which totals over 7 seconds, compare to `timing-report.txt`.

## Profile output - 5 calls to each function

<details>
<summary>cProfile output</summary>

```
Begin cProfile
Profiling python color2gray with cprofile:
         36 function calls in 3.415 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    3.372    0.674    3.415    0.683 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/python_filters.py:6(python_color2gray)
        5    0.043    0.009    0.043    0.009 {method 'tolist' of 'numpy.ndarray' objects}
        5    0.000    0.000    0.000    0.000 {built-in method numpy.empty}
       20    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numpy color2gray with cprofile:
         6 function calls in 0.011 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.011    0.002    0.011    0.002 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numpy_filters.py:5(numpy_color2gray)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numba color2gray with cprofile:
         11 function calls in 0.002 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.002    0.000    0.002    0.000 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numba_filters.py:7(numba_color2gray)
        5    0.000    0.000    0.000    0.000 /home/fredrik/.local/lib/python3.9/site-packages/numba/core/serialize.py:29(_numba_unpickle)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling cython color2gray with cprofile:
         111 function calls in 0.011 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.011    0.002    0.011    0.002 instapy/cython_filters.pyx:20(cython_color2gray)
        5    0.000    0.000    0.000    0.000 stringsource:1001(memoryview_fromslice)
       15    0.000    0.000    0.000    0.000 stringsource:659(memoryview_cwrapper)
       20    0.000    0.000    0.000    0.000 stringsource:346(__cinit__)
       20    0.000    0.000    0.000    0.000 stringsource:299(align_pointer)
       20    0.000    0.000    0.000    0.000 stringsource:374(__dealloc__)
       15    0.000    0.000    0.000    0.000 stringsource:665(memoryview_check)
        5    0.000    0.000    0.000    0.000 stringsource:978(__dealloc__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        5    0.000    0.000    0.000    0.000 stringsource:561(__get__)


Profiling python color2sepia with cprofile:
         46 function calls in 26.976 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5   26.028    5.206   26.976    5.395 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/python_filters.py:31(python_color2sepia)
        5    0.947    0.189    0.947    0.189 {method 'tolist' of 'numpy.ndarray' objects}
        5    0.000    0.000    0.000    0.000 {built-in method numpy.empty}
       30    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numpy color2sepia with cprofile:
         46 function calls in 0.060 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.057    0.011    0.060    0.012 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numpy_filters.py:20(numpy_color2sepia)
        5    0.000    0.000    0.004    0.001 <__array_function__ internals>:177(amax)
        5    0.000    0.000    0.004    0.001 {built-in method numpy.core._multiarray_umath.implement_array_function}
        5    0.000    0.000    0.004    0.001 /home/fredrik/.local/lib/python3.9/site-packages/numpy/core/fromnumeric.py:2677(amax)
        5    0.000    0.000    0.004    0.001 /home/fredrik/.local/lib/python3.9/site-packages/numpy/core/fromnumeric.py:69(_wrapreduction)
        5    0.004    0.001    0.004    0.001 {method 'reduce' of 'numpy.ufunc' objects}
        5    0.000    0.000    0.000    0.000 /home/fredrik/.local/lib/python3.9/site-packages/numpy/core/fromnumeric.py:70(<dictcomp>)
        5    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        5    0.000    0.000    0.000    0.000 /home/fredrik/.local/lib/python3.9/site-packages/numpy/core/fromnumeric.py:2672(_amax_dispatcher)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numba color2sepia with cprofile:
         11 function calls in 0.029 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.029    0.006    0.029    0.006 /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numba_filters.py:30(numba_color2sepia)
        5    0.000    0.000    0.000    0.000 /home/fredrik/.local/lib/python3.9/site-packages/numba/core/serialize.py:29(_numba_unpickle)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling cython color2sepia with cprofile:
         111 function calls in 0.111 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        5    0.111    0.022    0.111    0.022 instapy/cython_filters.pyx:54(cython_color2sepia)
        5    0.000    0.000    0.000    0.000 stringsource:1001(memoryview_fromslice)
       20    0.000    0.000    0.000    0.000 stringsource:346(__cinit__)
       15    0.000    0.000    0.000    0.000 stringsource:659(memoryview_cwrapper)
       20    0.000    0.000    0.000    0.000 stringsource:299(align_pointer)
       20    0.000    0.000    0.000    0.000 stringsource:374(__dealloc__)
       15    0.000    0.000    0.000    0.000 stringsource:665(memoryview_check)
        5    0.000    0.000    0.000    0.000 stringsource:978(__dealloc__)
        5    0.000    0.000    0.000    0.000 stringsource:561(__get__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


End cProfile
```

</details>

<details>
<summary>line_profiler output</summary>

```
Begin line_profiler
Profiling python color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 5.65839 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/python_filters.py
Function: python_color2gray at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           def python_color2gray(image: list, weights: list, k: Optional[float]) -> list:
     7                                               """Convert rgb pixel array to grayscale
     8                                           
     9                                               Args:
    10                                                   image (list): the original image array
    11                                                   weights (list): the weights of the transformation
    12                                                   k (float): amount of filter to apply (optional)
    13                                               Returns:
    14                                                   list: gray_image, the transformed image
    15                                               """
    16                                               
    17                                               #initialize empty filtered array to assigne values to
    18                                               # reduce RGB to grayscale (y,x,3) -> (y,x) as they are uniform
    19         5      44194.0   8838.8      0.8      gray_image = np.empty((len(image), len(image[0]))).tolist()
    20                                           
    21         5         21.0      4.2      0.0      H = len(gray_image) # 400
    22         5          9.0      1.8      0.0      W = len(gray_image[0]) # 600
    23                                               # iterate through the pixels, and apply the grayscale transform
    24      2405       1256.0      0.5      0.0      for i in range(H):
    25   1538400     736951.0      0.5     13.0          for j in range(W):
    26   1536000    4875959.0      3.2     86.2              gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    27                                               
    28         5          5.0      1.0      0.0      return gray_image

Profiling numpy color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 0.011882 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numpy_filters.py
Function: numpy_color2gray at line 5

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           def numpy_color2gray(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
     6                                               """Convert rgb pixel array to grayscale
     7                                           
     8                                               Args:
     9                                                   image (np.array): the original image array
    10                                                   weights (np.array): the weights of the transformation
    11                                                   k (float): amount of filter to apply (optional)
    12                                               Returns:
    13                                                   np.array: gray_image, the transformed image
    14                                               """
    15                                               # vectorized implementation of gray pure Python filter, slower than np.matmul.
    16                                               # image[:,:,0]*weights[0] + image[:,:,1]*weights[1] + image[:,:,2]*weights[2] # identical to np.dot(image, weights)
    17                                               
    18         5      11882.0   2376.4    100.0      return image @ weights #matrix multiplication using np.matmul

Profiling numba color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 0 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numba_filters.py
Function: numba_color2gray at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @njit(fastmath=True, parallel=True)
     8                                           def numba_color2gray(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
     9                                               """Convert rgb pixel array to grayscale
    10                                           
    11                                               Args:
    12                                                   image (np.array): the original image array
    13                                                   weights (np.array): the weights of the transformation
    14                                                   k (float): amount of filter to apply (optional)
    15                                               Returns:
    16                                                   np.array: gray_image, the transformed image
    17                                               """
    18                                               
    19                                               #initialize empty filtered array to assigne values to
    20                                               #reduce RGB to grayscale (y,x,3) -> (y,x) as they are uniform, massive speedup
    21                                               gray_image = np.empty(image.shape[0:2]) 
    22                                           
    23                                               # same as: np.dot(image, weights)
    24                                               for i in prange(image.shape[0]):
    25                                                   for j in prange(image.shape[1]):
    26                                                       gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    27                                               
    28                                               return gray_image

Profiling cython color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 0.483901 s
File: instapy/cython_filters.pyx
Function: cython_color2gray at line 20

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    20                                           def cython_color2gray(const np.npy_uint8[:,:,::1] image, const double[::1] weights, k: Optional[float] = 1) -> np.array:
    21                                               """Convert rgb pixel array to grayscale
    22                                           
    23                                               Args:
    24                                                   image (np.array): the original image array
    25                                                   weights (np.array): the weights of the transformation
    26                                                   k (float): amount of filter to apply (optional)
    27                                               Returns:
    28                                                   np.array: gray_image, the transformed image
    29                                               """
    30                                               
    31                                               # creates native c index/loop variable
    32         5          6.0      1.2      0.0      cdef size_t H = image.shape[0]
    33         5          5.0      1.0      0.0      cdef size_t W = image.shape[1]
    34                                           
    35                                               # C contiguous [::1] (numpy like) memoryviews [:,:] (cython vectorized array)
    36                                               # for more info: https://docs.cython.org/en/latest/src/userguide/numpy_tutorial.html
    37         5         47.0      9.4      0.0      g = np.empty((H,W), dtype=DTYPE)
    38         5         21.0      4.2      0.0      cdef double[:,::1] gray_image = g 
    39                                           
    40                                               cdef size_t i, j
    41         5          2.0      0.4      0.0      for i in range(H):
    42      2400        768.0      0.3      0.2          for j in range(W):
    43   1536000     482956.0      0.3     99.8              gray_image[i][j] = image[i][j][0]*weights[0] + image[i][j][1]*weights[1] + image[i][j][2]*weights[2]
    44                                               
    45         5         96.0     19.2      0.0      return gray_image

Profiling python color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 52.523 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/python_filters.py
Function: python_color2sepia at line 31

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    31                                           def python_color2sepia(image: list, weights: list, k: Optional[float] = 1) -> list:
    32                                               """Convert rgb pixel array to sepia
    33                                           
    34                                               Args:
    35                                                   image (list): the original image array
    36                                                   weights (list): the weights of the transformation
    37                                                   k (float): amount of filter to apply (optional)
    38                                               Returns:
    39                                                   list: sepia_image, the transformed image
    40                                               """
    41         5         19.0      3.8      0.0      if not 0 <= k <= 1:
    42                                                   # validate k (optional)
    43                                                   raise ValueError(f"k must be between [0-1], got {k=}")
    44                                           
    45         5     979925.0 195985.0      1.9      sepia_image = np.empty((len(image), len(image[0]), len(image[0][0]))).tolist()
    46         5         15.0      3.0      0.0      max = 0
    47                                           
    48         5         15.0      3.0      0.0      H = len(sepia_image) # 400
    49         5          9.0      1.8      0.0      W = len(sepia_image[0]) # 600
    50         5          4.0      0.8      0.0      D = len(sepia_image[0][0]) # 3
    51                                               # iterate through the pixels, and apply the sepia transform
    52      2405       1574.0      0.7      0.0      for i in range(H):
    53   1538400     876427.0      0.6      1.7          for j in range(W):
    54   6144000    4004462.0      0.7      7.6              for l in range(D):
    55   4608000   16841818.0      3.7     32.1                  val = (weights[l][0]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][2]*image[i][j][2]) 
    56                                           
    57   4608000   17377745.0      3.8     33.1                  sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    58                                                           
    59   4608000    3505087.0      0.8      6.7                  if sepia_image[i][j][l] > max:
    60        70         57.0      0.8      0.0                      max = sepia_image[i][j][l]
    61                                           
    62                                               # new looop now that max is properly defined
    63      2405       1408.0      0.6      0.0      for i in range(H):
    64   1538400     837725.0      0.5      1.6          for j in range(W):
    65   6144000    3735347.0      0.6      7.1              for l in range(D):
    66   4608000    4361373.0      0.9      8.3                  sepia_image[i][j][l] = sepia_image[i][j][l]/max*255
    67                                           
    68                                           
    69         5          5.0      1.0      0.0      return sepia_image

Profiling numpy color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 0.058003 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numpy_filters.py
Function: numpy_color2sepia at line 20

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    20                                           def numpy_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    21                                               """Convert rgb pixel array to sepia
    22                                           
    23                                               Args:
    24                                                   image (np.array): the original image array
    25                                                   weights (np.array): the weights of the transformation
    26                                                   k (float): amount of filter to apply (optional)
    27                                               Returns:
    28                                                   np.array: sepia_image, the transformed image
    29                                               """
    30                                           
    31         5         17.0      3.4      0.0      if not 0 <= k <= 1:
    32                                                   # validate k (optional)
    33                                                   raise ValueError(f"k must be between [0-1], got {k=}")
    34                                               # vectorized implementation of the sepia transform
    35         5      45789.0   9157.8     78.9      image = image * (1-k) + image @ weights.T * k
    36                                           
    37         5      12197.0   2439.4     21.0      return image/np.max(image)*255

Profiling numba color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 0 s
File: /home/fredrik/Documents/IN4110/IN3110-fredhof/assignment3/instapy/numba_filters.py
Function: numba_color2sepia at line 30

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    30                                           @njit(fastmath=True, parallel = True)
    31                                           def numba_color2sepia(image: np.array, weights: np.array, k: Optional[float] = 1) -> np.array:
    32                                               """Convert rgb pixel array to sepia
    33                                           
    34                                               Args:
    35                                                   image (np.array): the original image array
    36                                                   weights (np.array): the weights of the transformation
    37                                                   k (float): amount of filter to apply (optional)
    38                                               Returns:
    39                                                   np.array: sepia_image, the transformed image
    40                                               """
    41                                               if not 0 <= k <= 1:
    42                                                   # validate k (optional)
    43                                                   raise ValueError("k must be between [0-1]")
    44                                           
    45                                               #initialize empty filtered array to assigne values to
    46                                               sepia_image = np.empty(image.shape)
    47                                           
    48                                               # weights needs to be transposed for summation to work nicely
    49                                               # same as: image * (1-k) + np.dot(image, weights.T) * k, if k=0 it reduces to image, if k=1 it reduces to np.dot(image, weights.T)
    50                                               for i in prange(image.shape[0]):
    51                                                   for j in prange(image.shape[1]):
    52                                                       for l in prange(image.shape[2]):
    53                                                           val = weights[l][0]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][2]*image[i][j][2]
    54                                                           
    55                                                           sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    56                                               
    57                                               # not parallelized since it will cause issues.
    58                                               maxx = 0  
    59                                               for i in range(image.shape[0]):
    60                                                   for j in range(image.shape[1]):
    61                                                       for l in range(image.shape[2]):
    62                                                           if sepia_image[i][j][l] > maxx:
    63                                                               maxx = sepia_image[i][j][l] 
    64                                           
    65                                               # normalizes the array so it can be transformed to uint8 without loss
    66                                               for i in prange(image.shape[0]):
    67                                                   for j in prange(image.shape[1]):
    68                                                       for l in prange(image.shape[2]):     
    69                                                           sepia_image[i][j][l] = sepia_image[i][j][l]/maxx*255
    70                                           
    71                                           
    72                                               return sepia_image

Profiling cython color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 7.73063 s
File: instapy/cython_filters.pyx
Function: cython_color2sepia at line 54

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    54                                           def cython_color2sepia(const np.npy_uint8[:,:,::1] image, const double[:,::1] weights, const double k = 1) -> np.array:
    55                                               """Convert rgb pixel array to sepia
    56                                               
    57                                               Args:
    58                                                   image (np.array): the original image array
    59                                                   weights (np.array): the weights of the transformation
    60                                                   k (float): amount of filter to apply (optional)
    61                                               Returns:
    62                                                   np.array: sepia_image, the transformed image
    63                                               """
    64                                           
    65         5          6.0      1.2      0.0      if not 0 <= k <= 1:
    66                                                   # validate k (optional)
    67                                                   raise ValueError("k must be between [0-1]")
    68                                               
    69                                               # creates native c index/loop variable
    70         5          4.0      0.8      0.0      cdef size_t H = image.shape[0]
    71         5          4.0      0.8      0.0      cdef size_t W = image.shape[1]
    72         5          3.0      0.6      0.0      cdef size_t D = image.shape[2]
    73                                           
    74                                               # C contiguous [::1] (numpy like) memoryviews [:,:] (cython vectorized array)
    75                                               # for more info: https://docs.cython.org/en/latest/src/userguide/numpy_tutorial.html
    76         5         74.0     14.8      0.0      s = np.empty((H,W,D), dtype=DTYPE)
    77         5         22.0      4.4      0.0      cdef double[:,:,::1] sepia_image = s 
    78                                           
    79                                               cdef size_t i, j, l
    80                                               cdef double val, maxx
    81                                               
    82                                               # iterate through the pixels, and apply the sepia transform
    83         5          1.0      0.2      0.0      for i in range(H):
    84      2400        875.0      0.4      0.0          for j in range(W):
    85   1536000     543334.0      0.4      7.0              for l in range(D):
    86   4608000    1635758.0      0.4     21.2                  val = weights[l][0]*image[i][j][0] + weights[l][1]*image[i][j][1] + weights[l][2]*image[i][j][2]
    87                                           
    88   4608000    1630550.0      0.4     21.1                  sepia_image[i][j][l] = image[i][j][l] * (1-k) + val * k
    89                                               
    90   4608000    1663950.0      0.4     21.5                  if sepia_image[i][j][l] > maxx:
    91        70         34.0      0.5      0.0                      maxx = sepia_image[i][j][l] 
    92                                                               
    93                                               # new looop now that max is properly defined
    94         5          3.0      0.6      0.0      for i in range(H):
    95      2400        885.0      0.4      0.0          for j in range(W):
    96   1536000     548048.0      0.4      7.1              for l in range(D):
    97   4608000    1706970.0      0.4     22.1                  sepia_image[i][j][l] = sepia_image[i][j][l]/maxx*255
    98                                           
    99         5        111.0     22.2      0.0      return sepia_image

End line_profiler

```

</details>
