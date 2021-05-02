#! /usr/bin/env python

import numpy as np
import argparse
import sys
import time
import math
from multiprocessing import Pool, TimeoutError


def compute_julia_set_sequential(xmin, xmax, ymin, ymax, im_width, im_height, metadata):

    zabs_max = 10
    c = complex(-0.1, 0.65)
    nit_max = 1000

    xwidth = xmax - xmin
    yheight = ymax - ymin

    julia = np.zeros((im_width, im_height))
    for ix in range(im_width):
        for iy in range(im_height):
            nit = 0
            # Map pixel position to a point in the complex plane
            z = complex(ix / im_width * xwidth + xmin, iy / im_height * yheight + ymin)
            # Do the iterations
            while abs(z) <= zabs_max and nit < nit_max:
                z = z ** 2 + c
                nit += 1
            ratio = nit / nit_max
            julia[ix, iy] = ratio

    return julia, metadata


def compute_julia_in_parallel(size, xmin, xmax, ymin, ymax, patch, nprocs):

    pool = Pool(processes=nprocs)

    scaled_width = xmax - xmin
    scaled_height = ymax - ymin

    x_ratio = scaled_width / size
    y_ratio = scaled_height / size

    scaled_patch_x = patch * x_ratio
    scaled_patch_y = patch * y_ratio

    num_patches_x = math.floor(scaled_width / scaled_patch_x) + 1
    num_patches_y = math.floor(scaled_height / scaled_patch_y) + 1

    inputs = []

    i = 0
    y_max_i = ymax
    y_min_i = ymax - scaled_patch_y
    for patch_col in range(num_patches_y):

        j = 0
        x_min_j = xmin
        x_max_j = xmin + scaled_patch_x

        y_patch = patch
        if patch_col + 1 == num_patches_y:
            y_patch = size - (num_patches_y-1) * patch

        for patch_row in range(num_patches_x):

            x_patch = patch
            if patch_row + 1 == num_patches_x:
                x_patch = size - (num_patches_x - 1) * patch

            metadata = (i, j)
            arguments = (x_min_j, x_max_j, y_min_i, y_max_i, x_patch, y_patch, metadata)
            inputs.append(arguments)

            x_min_j = x_max_j
            if patch_row + 2 == num_patches_x:
                x_max_j = xmax
            else:
                x_max_j += scaled_patch_x
            j += 1

        y_max_i = y_min_i
        if patch_col + 2 == num_patches_y:
            y_min_i = ymin
        else:
            y_min_i -= scaled_patch_y

        i += 1

    completed_tasks = pool.starmap(compute_julia_set_sequential, inputs, chunksize=1)
    pool.close()

    pool.join()

    completed_tasks.sort(key=lambda t: t[1])
    images = [task[0] for task in completed_tasks]

    row_images = []

    for row in range(num_patches_x, num_patches_x*num_patches_y + 1, num_patches_x):
        row_image = np.concatenate(images[row-num_patches_x:row], axis=0)
        row_images.append(row_image)

    full_image = np.concatenate(list(reversed(row_images)), axis=1)

    return full_image


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size", help="image size in pixels (square images)", type=int, default=500
    )
    parser.add_argument("--xmin", help="", type=float, default=-1.5)
    parser.add_argument("--xmax", help="", type=float, default=1.5)
    parser.add_argument("--ymin", help="", type=float, default=-1.5)
    parser.add_argument("--ymax", help="", type=float, default=1.5)
    parser.add_argument(
        "--patch", help="patch size in pixels (square images)", type=int, default=20
    )
    parser.add_argument("--nprocs", help="number of workers", type=int, default=1)
    parser.add_argument("-o", help="output file")
    args = parser.parse_args()

    if args.patch > args.size:
        print(f"Patch {[args.patch]} should be smaller than size {[args.size]}")
        sys.exit(1)

    stime = time.perf_counter()
    julia_img = compute_julia_in_parallel(
        args.size, args.xmin, args.xmax, args.ymin, args.ymax, args.patch, args.nprocs
    )
    rtime = time.perf_counter() - stime

    print(f"{args.size};{args.patch};{args.nprocs};{rtime}")

    if not args.o is None:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.imshow(julia_img, interpolation="nearest", cmap=plt.get_cmap("hot"))
        plt.savefig(args.o)
        plt.show()
