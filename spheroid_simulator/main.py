from point import Point
from spheroid import Spheroid
from skimage.draw import line, line_aa
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':

    img_size = 1304
    centroid =Point(img_size/2, img_size/2)
    spheroid = Spheroid(centroid, neuron_number=200, cover_angle=360, min_radius=10, max_radius=600, offset_delta=2, division_nb=3)
    spheroid.create_neurons()
    spheroid.add_random_neurons(10)


    img = np.zeros((img_size, img_size))
    for neuron in spheroid.neuron_list:
        for seg in neuron.segmentList:
            rr, cc, val = line_aa(seg.startPoint.x, seg.startPoint.y, seg.endPoint.x, seg.endPoint.y)
            img[rr, cc] = val * neuron.intensity
    plt.figure(dpi=1200)
    plt.imsave("200n_1200dpi.png", img, cmap="gray")

