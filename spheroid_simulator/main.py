import copy
import os.path
import pathlib
import random

import numpy as np
from artifacts import Artifacts
from background import Background
# from matplotlib import pyplot as plt
from nucleus import Nucleus
from point import Point
from skimage import draw, io
from skimage.exposure import rescale_intensity
from spheroid import Spheroid
from tqdm import tqdm

if __name__ == "__main__":

    img_size = 1024
    anti_aliasing_threshold = 9
    out_folder_name = "test_upgrade"
    img_size_percent = int((img_size / 100) * 5)
    for idx in tqdm(range(2000, 3000)):
        nucleus_size = random.randint(50, 80)
        #  461 <= x <= 563
        x = (img_size / 2) + random.randint(-img_size_percent, img_size_percent)
        y = (img_size / 2) + random.randint(-img_size_percent, img_size_percent)
        centroid = Point(x, y)
        spheroid = Spheroid(
            centroid=centroid,
            neuron_number=random.randint(150, 250),
            cover_angle=360,
            min_max_radius=[
                random.randint(10, 40),
                random.randint(350, img_size - x - 1),
            ],
            offset_delta=[2, 4],
            division_nb=[2, 4],
            min_max_intensity=[random.randint(50, 70), random.randint(130, 180)],
        )

        spheroid.create_neurons()
        spheroid.add_random_neurons(random.randint(5, 10))

        perlin_noise_level = random.choice([2, 4, 8, 16])
        poisson_noise_level = random.randint(50, 100)
        perlin_out_range = random.randint(50, 100)
        full_noise_level = random.randint(80, 100)
        smooth_sigma = random.randint(1, 3)

        img = Background(
            img_size,
            perlin_noise_level,
            poisson_noise_level,
            perlin_out_range,
            full_noise_level,
        )
        img.create_background()
        # img.smooth_background(smooth_sigma)
        enhanced = copy.deepcopy(img)

        ################################
        # #### Apply elastic transform on noise
        # cmin = int(norm_sum_noise.shape[0] / 2 - img_size / 2)
        # cmax = int(norm_sum_noise.shape[0] / 2 + img_size / 2)
        # crop = (slice(cmin, cmax), slice(cmin, cmax))
        # noise_elastic = elasticdeform.deform_random_grid(
        # norm_sum_noise, sigma=random.randint(10, 20),
        # points=random.randint(2, 6), crop=crop)
        # full_noise = rescale_intensity(noise_elastic,
        # out_range=(0, full_noise_level))
        #
        # target = img.copy()
        # img += full_noise
        # img = rescale_intensity(img, out_range=(0, 255))

        ################################

        for neuron in spheroid.neuron_list:
            if neuron.anti_aliasing > anti_aliasing_threshold:
                for seg in neuron.segmentList:
                    rr, cc, val = draw.line_aa(
                        seg.startPoint.x,
                        seg.startPoint.y,
                        seg.endPoint.x,
                        seg.endPoint.y,
                    )
                    img.noise_map[rr, cc] = val * neuron.intensity
                    enhanced.noise_map[rr, cc] = 250
            else:
                for seg in neuron.segmentList:
                    rr, cc = draw.line(
                        seg.startPoint.x,
                        seg.startPoint.y,
                        seg.endPoint.x,
                        seg.endPoint.y,
                    )
                    # if rr.any() < img_size and cc.any() < img_size:
                    img.noise_map[rr, cc] = neuron.intensity
                    enhanced.noise_map[rr, cc] = 250

        artifacts = Artifacts(
            img_size=img_size,
            artifacts_nb=random.randint(10, 50),
            intensity=spheroid.min_max_intensity,
        )
        artifacts.create_artifacts_map()
        enhanced.noise_map = enhanced.noise_map + artifacts.artifacts_map
        img.noise_map = img.noise_map + artifacts.artifacts_map

        enhanced.noise_map = rescale_intensity(enhanced.noise_map, out_range=(0, 255))
        img.noise_map = rescale_intensity(img.noise_map, out_range=(0, 255))

        nucl = Nucleus(
            kernel_size=20,
            std=4,
            image_size=img_size,
            radius=nucleus_size,
            centroid=centroid,
        )
        nucl.create_nucleus()
        result = img.noise_map * nucl.nucleus
        enhanced = enhanced.noise_map * nucl.nucleus

        enhanced = rescale_intensity(enhanced, out_range=(0, 255))
        result = rescale_intensity(result, out_range=(0, 255))

        # plt.figure(dpi=600)
        # plt.imsave("nucleus.png", nucl.nucleus, cmap="gray")

        root = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        pathlib.Path(os.path.join(root, "data", out_folder_name, "images")).mkdir(
            parents=True, exist_ok=True
        )
        pathlib.Path(os.path.join(root, "data", out_folder_name, "target")).mkdir(
            parents=True, exist_ok=True
        )

        io.imsave(
            os.path.join(root, "data", out_folder_name, "images", str(idx) + ".png"),
            result.astype(np.uint8),
        )
        io.imsave(
            os.path.join(root, "data", out_folder_name, "target", str(idx) + ".png"),
            enhanced.astype(np.uint8),
        )
