# -*- coding: utf-8 -*-
# /usr/bin/python3.9

# import cv2
# import elasticdeform
import numpy as np
from skimage.exposure import rescale_intensity


class Background:
    """Background definition"""

    def __init__(
        self,
        img_size,
        perlin_noise_level,
        poisson_noise_level,
        perlin_out_range,
        full_noise_level,
    ):
        self.perlin_noise_level = perlin_noise_level
        self.poisson_noise_level = poisson_noise_level
        self.perlin_out_range = perlin_out_range
        self.full_noise_level = full_noise_level
        self.img_size = img_size
        self.noise_map = np.zeros((self.img_size, self.img_size))

    def create_background(self):
        ### Rescale Poisson noise
        self.poisson_noise = np.random.normal(
            loc=0, scale=1, size=(self.img_size, self.img_size)
        )
        self.poisson_noise = rescale_intensity(
            self.poisson_noise, out_range=(0, self.poisson_noise_level)
        )

        #### Generate perlin noise
        self.perlin_noise = self.generate_fractal_noise_2d(
            (self.img_size, self.img_size),
            (self.perlin_noise_level, self.perlin_noise_level),
            5,
        )
        self.perlin_noise = rescale_intensity(
            self.perlin_noise, out_range=(0, self.perlin_out_range)
        )

        #### Normalize noise
        self.sum_noise = self.perlin_noise + self.poisson_noise
        self.noise_map = rescale_intensity(
            self.sum_noise, out_range=(0, self.full_noise_level)
        )

    def generate_perlin_noise_2d(self, shape, res):
        def f(t):
            return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

        delta = (res[0] / shape[0], res[1] / shape[1])
        d = (shape[0] // res[0], shape[1] // res[1])
        grid = (
            np.mgrid[0 : res[0] : delta[0], 0 : res[1] : delta[1]].transpose(1, 2, 0)
            % 1
        )
        # Gradients
        angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
        g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
        # Ramps
        n00 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1])) * g00, 2)
        n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
        n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
        # Interpolation
        t = f(grid)
        n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
        n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
        return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

    def generate_fractal_noise_2d(self, shape, res, octaves=1, persistence=0.5):
        noise = np.zeros(shape)
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            noise += amplitude * self.generate_perlin_noise_2d(
                shape, (frequency * res[0], frequency * res[1])
            )
            frequency *= 2
            amplitude *= persistence

        return noise
