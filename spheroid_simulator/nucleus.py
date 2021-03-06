import numpy as np
import scipy.stats as st
from scipy import signal


class Nucleus:
    """Definition d'un Noyau"""

    def __init__(self, kernel_size, std, image_size, radius, centroid):
        self.mask = None
        self.nucleus = None
        self.kernel = None
        self.kernel_size = kernel_size
        self.std = std
        self.image_size = image_size
        self.radius = radius
        self.centroid = centroid

    def create_nucleus(self):
        """Returns a 2D Gaussian kernel."""
        # ---- Create a 1D kernel of size kernel_size between values -std and std
        x = np.linspace(-self.std, self.std, self.kernel_size + 1)
        # ---- Calculate the difference between
        # subsequent values over the cumulative distribution
        kernel_1d = np.diff(st.norm.cdf(x))
        # --- Goes 2D by the product of the kernel 1D by himself
        kernel_2d = np.outer(kernel_1d, kernel_1d)
        # normalize and return
        self.kernel = kernel_2d / kernel_2d.sum()
        self.create_circular_mask()
        self.nucleus = signal.convolve2d(self.mask, self.kernel, mode="same")
        self.nucleus = 1 - self.nucleus

    def create_circular_mask(self):
        Y, X = np.ogrid[: self.image_size, : self.image_size]
        dist_from_center = np.sqrt(
            (X - self.centroid.y) ** 2 + (Y - self.centroid.x) ** 2
        )
        self.mask = dist_from_center <= self.radius
