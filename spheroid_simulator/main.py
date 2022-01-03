import random

from background import Background
from matplotlib import pyplot as plt
from nucleus import Nucleus
from point import Point
from skimage import draw
from spheroid import Spheroid

if __name__ == "__main__":

    img_size = 1024
    nucleus_size = random.randint(50, 100)
    centroid = Point(img_size / 2, img_size / 2)
    spheroid = Spheroid(
        centroid,
        neuron_number=100,
        cover_angle=360,
        min_radius=10,
        max_radius=500,
        offset_delta=2,
        division_nb=3,
    )
    spheroid.create_neurons()
    spheroid.add_random_neurons(random.randint(5, 10))

    perlin_noise_level = random.choice([2, 4, 8, 16])
    poisson_noise_level = random.randint(50, 100)
    perlin_out_range = random.randint(50, 100)
    full_noise_level = random.randint(80, 150)

    img = Background(
        img_size,
        perlin_noise_level,
        poisson_noise_level,
        perlin_out_range,
        full_noise_level,
    )
    img.create_background()

    #
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
        for seg in neuron.segmentList:
            rr, cc, val = draw.line_aa(
                seg.startPoint.x, seg.startPoint.y, seg.endPoint.x, seg.endPoint.y
            )
            img.noise_map[rr, cc] = val * neuron.intensity

    nucl = Nucleus(20, 4, img_size, nucleus_size)
    nucl.create_nucleus()
    result = img.noise_map * nucl.nucleus

    plt.figure(dpi=1200)
    plt.imsave("test.png", result, cmap="gray")
