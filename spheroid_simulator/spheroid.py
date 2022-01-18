import math
import random

from neuron import Neuron
from point import Point
from segment import Segment


class Spheroid:
    """Definition d'un spheroide"""

    def __init__(
        self,
        centroid,
        neuron_number,
        cover_angle,
        min_max_radius,
        offset_delta,
        division_nb,
        min_max_intensity,
    ):

        self.centroid = centroid
        self.neuron_number = neuron_number
        self.cover_angle = cover_angle
        self.min_max_radius = min_max_radius
        self.offset_delta = offset_delta
        self.division_nb = division_nb
        self.min_max_intensity = min_max_intensity
        self.start_list = []
        self.stop_list = []
        self.neuron_list = []
        self.mask = None

    def create_start_and_stop(self, radius):
        # Non linear distribution arround self.centroid
        # Random angle between o and max_angle
        max_angle = (self.cover_angle * 2 * math.pi) / 360
        angle = max_angle * random.random()
        # random radius size between 0 and radius. SQRT use for avec less short radius
        r = radius * math.sqrt(random.random())
        # coordinates centered on x,y
        x = r * math.cos(angle) + self.centroid.x
        y = r * math.sin(angle) + self.centroid.y
        return Point(x, y)

    def create_neurons(self):
        for _ in range(self.neuron_number):
            start = Spheroid.create_start_and_stop(self, self.min_max_radius[0])
            stop = Spheroid.create_start_and_stop(self, self.min_max_radius[1])
            neuronino = Segment(start, stop)
            n = Neuron(
                neuronino.startPoint,
                neuronino.endPoint,
                random.randint(self.offset_delta[0], self.offset_delta[1]),
                random.randint(self.division_nb[0], self.division_nb[1]),
                random.randint(self.min_max_intensity[0], self.min_max_intensity[1]),
                anti_aa=random.randint(0, 10),
            )
            n.make_neuron()
            n.interpolate_neuron()
            self.neuron_list.append(n)

    def add_random_neurons(self, random_neuron_number):
        self.random_neuron_number = random_neuron_number
        for _ in range(random_neuron_number):
            start = Point(random.randint(10, 1000), random.randint(10, 1000))
            stop = Point(random.randint(10, 1000), random.randint(10, 1000))
            neuronino = Segment(start, stop)
            n = Neuron(
                neuronino.startPoint,
                neuronino.endPoint,
                random.randint(self.offset_delta[0], self.offset_delta[1]),
                random.randint(self.division_nb[0], self.division_nb[1]),
                random.randint(self.min_max_intensity[0], self.min_max_intensity[1]),
                anti_aa=random.randint(0, 10),
            )
            n.make_neuron()
            n.interpolate_neuron()
            self.neuron_list.append(n)
