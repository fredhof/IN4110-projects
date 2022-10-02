"""Command-line (script) interface to instapy"""

import argparse

import numpy as np
from PIL import Image

import instapy
from instapy import io, python_filters, numpy_filters, numba_filters, cython_filters
from instapy.timing import time_one


def run_filter(
    file: str,
    out_file = None,
    implementation: str = "python",
    filter = None,
    scale: int = None,
    k: float = 1.,
    runtime: int = 5,
    return_array: bool = False
) -> None:
    """Run the selected filter"""
    # load the image from a file
    if isinstance(file, np.ndarray): image_array = file #if file is an array, skip loading image
    else:
        image = Image.open(file)
        image_array = np.array(image)

    # Resizes image if needed
    if scale != None:
            # if image doesnt exist loads from array, used if both filters are applied, see line where ' inp == "yes" '
            try:
                image
            except NameError:
                image = Image.fromarray(np.uint8(image_array))

            image = image.resize((np.array(image.size)*scale).astype(np.int32))
            image_array = np.array(image)

    if filter == None: filtered = image_array
    else: 

        if "python" in implementation: implementation_func = python_filters
        if "numpy" in implementation: implementation_func = numpy_filters
        if "numba" in implementation: implementation_func = numba_filters
        if "cython" in implementation: implementation_func = cython_filters

        if "gray" in filter:
            filter = "gray"

            # getattr finds the function callable from the implementation file
            filter_func = getattr(implementation_func, implementation + "_color2" + filter)
            weights = np.array([0.21, 0.72, 0.07])

        if "sepia" in filter:
            filter = "sepia"
            filter_func = getattr(implementation_func, implementation + "_color2" + filter)
            weights = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])


        # Apply the filter
        filtered = filter_func(image_array, weights, k)

    if return_array: return filtered
    
    if runtime:
        print(f"The average time of {filter_func} over {runtime} runs was: {time_one(filter_func, image, weights, k):.3g}s ")

    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(np.uint8(filtered))


def main():
    """Parse the command-line and call run_filter with the arguments"""

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    
    # Add required arguments
    parser.add_argument("-o", "--out", help="The output filename")
    parser.add_argument("-g", "--gray", action='store_true', default=argparse.SUPPRESS, help="Transform with the gray filter")
    parser.add_argument("-se", "--sepia", action='store_true', default=argparse.SUPPRESS, help="Transform with the sepia filter")
    parser.add_argument("-k", "--k", action='store', type=float, help="The scaling of the transformation. k=0 gives the original image, k=1 (default) gives the transformed image. Currently only supports sepia scaling.")
    parser.add_argument("-sc", "--scale", action='store', type=float, help="Uniformly scale the size of the image by a constant")
    parser.add_argument("-i", "--implementation", default="python", help="Specify implementation. Supports: python, numpy, numba, cython.")
    parser.add_argument("-r,", "--runtime", action='store', type=int, nargs = "?", const = 5, default = None ,help="Tracks the average run time with timeit.timeit. Specify number of runs, default is 5.")

    # parse arguments and call run_filter
    args = parser.parse_args()

    if "gray" in args: filter = "gray"
    elif "sepia" in args: filter = "sepia"
    else: filter = None

    if "gray" in args and "sepia" in args:
        inp = input(f"Detected gray and sepia filter. Type \"1\" or \"2\" for the specific filter, \"yes\" for both applied consecutively or \"no\" for no filter.\
            \n[1 / 2 / yes / no]: ")
        
        if inp == "1": filter = "gray"

        elif inp == "2": filter = "sepia"

        elif inp == "yes":
            f1 = run_filter(args.file, args.out ,args.implementation, "gray", args.scale, args.k, args.runtime, return_array=True)
            f2 = np.empty_like(Image.open(args.file))
            for i in range(3): f2[:,:,i] = f1
            run_filter(f2, args.out, args.implementation, "sepia", args.scale, args.k, args.runtime)
            return

        elif inp == "no": filter = None
        else: raise Exception("Invalid input.")
    

    if not args.k is None:
        
        if "gray" in filter:
            print(f"Scaling the gray filter is currently not possible. Setting k=1...")
            args.k = 1

        if not 0 <= args.k <= 1:
            # validate k (optional)
            raise ValueError(f"k must be between [0-1], got {args.k=}")

    run_filter(args.file, args.out, args.implementation, filter, args.scale, args.k, args.runtime)


if __name__ == '__main__':
    main()