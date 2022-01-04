import copy
import os.path
import pathlib
import random

from background import Background
from nucleus import Nucleus
from point import Point
from skimage import draw, io
from spheroid import Spheroid

if __name__ == "__main__":

    img_size = 1024
    for idx in range(0, 5000):
        nucleus_size = random.randint(50, 80)
        centroid = Point(img_size / 2, img_size / 2)
        spheroid = Spheroid(
            centroid,
            neuron_number=200,
            cover_angle=360,
            min_radius=10,
            max_radius=500,
            offset_delta=2,
            division_nb=3,
            min_intensity=40,
            max_intensity=80,
        )

        spheroid.create_neurons()
        spheroid.add_random_neurons(random.randint(5, 10))

        perlin_noise_level = random.choice([2, 4, 8, 16])
        poisson_noise_level = random.randint(50, 100)
        perlin_out_range = random.randint(50, 100)
        full_noise_level = random.randint(100, 150)
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
            if neuron.anti_aliasing > 9:
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
                    img.noise_map[rr, cc] = neuron.intensity
                    enhanced.noise_map[rr, cc] = 250

        nucl = Nucleus(20, 4, img_size, nucleus_size)
        nucl.create_nucleus()
        result = img.noise_map * nucl.nucleus
        enhanced = enhanced.noise_map * nucl.nucleus

        # plt.figure(dpi=600)
        # plt.imsave("test.png", result, cmap="gray")

        root = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        pathlib.Path(os.path.join(root, "data", "images")).mkdir(
            parents=True, exist_ok=True
        )
        pathlib.Path(os.path.join(root, "data", "target")).mkdir(
            parents=True, exist_ok=True
        )

        io.imsave(os.path.join(root, "data", "images", str(idx) + ".png"), result)
        io.imsave(os.path.join(root, "data", "target", str(idx) + ".png"), enhanced)
