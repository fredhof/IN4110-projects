# Cython
To use the Cython filters, first generate the executable `.so` by running `python3 setup.py build-ext -i` in the directory of `setup.py` and then in Python do `import cython_filters`.

# Performance
With CPU `Intel Pentium 4415U (4) @ 2.3GHz`:  `timeit.timeit` times the (gray) Cython filter ~30% slower if it runs after Numba is compiled. Numba is ~5% slower if Cython runs before it is compiled.
It adds ~0.0001s to the time (~10% numba, 5% cython) if they are run before python and numpy.
Will test with another CPU:`AMD Ryzen 9 5600X (6) @ 3.7GHz`.