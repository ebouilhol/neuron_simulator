from random import randint, randrange

import numpy as np
import scipy.stats as st
from scipy import signal
from skimage.exposure import rescale_intensity


class Artifacts:
    """Add artifacts to images"""

    def __init__(self, img_size, artifacts_nb, intensity):
        self.img_size = img_size
        self.artifacts_nb = artifacts_nb
        self.intensity = intensity
        self.artifacts_map = None

    def random_unispots_coordinates(self):
        arr = np.zeros((self.img_size, self.img_size))
        x = randrange(2, self.img_size - 2)
        y = randrange(2, self.img_size - 2)
        arr[x][y] = 1

        return arr

    def gaussian_kernel(self, kernel_size, std):
        """Returns a 2D Gaussian kernel."""
        # ---- Create a 1D kernel of size kernel_size between values -std and std
        x = np.linspace(-std, std, kernel_size + 1)
        # ---- Calculate the differecence between subsequent
        # values over the cumulative distribution
        kernel_1d = np.diff(st.norm.cdf(x))
        # --- Goes 2D by the product of the kernel 1D by himself
        kernel_2d = np.outer(kernel_1d, kernel_1d)
        # normalize and return
        return kernel_2d / kernel_2d.sum()

    def create_artifacts_map(self):
        temp_map = self.random_unispots_coordinates()
        psf_kernel = self.gaussian_kernel(
            kernel_size=randint(13, 18), std=randint(3, 8)
        )
        self.artifacts_map = signal.convolve2d(temp_map, psf_kernel, mode="same")

        for _ in range(self.artifacts_nb):
            temp_map = self.random_unispots_coordinates()
            psf_kernel = self.gaussian_kernel(
                kernel_size=randint(13, 18), std=randint(3, 8)
            )
            temp_img = signal.convolve2d(temp_map, psf_kernel, mode="same")
            self.artifacts_map = self.artifacts_map + temp_img

        self.artifacts_map = rescale_intensity(
            self.artifacts_map, out_range=(0, self.intensity[1])
        )
        # self.artifacts_map = 1 + self.artifacts_map
