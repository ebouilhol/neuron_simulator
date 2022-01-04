# -*- coding: utf-8 -*-
# /usr/bin/python3.9
import random
from math import dist, sqrt

import numpy as np
from point import Point
from scipy.ndimage import gaussian_filter1d
from segment import Segment


class Neuron:
    """Definition d'un neuron"""

    def __init__(self, start, stop, offset_delta, div_number, intensity):
        self.start = start
        self.stop = stop
        self.offset_delta = offset_delta
        self.div_number = div_number
        self.segmentList = []
        self.intensity = intensity
        self.anti_aliasing = random.randint(0, 10)

    def find_offset(self, seg):
        offset_max = sqrt(
            dist((seg.startPoint.x, seg.startPoint.y), (seg.endPoint.x, seg.endPoint.y))
        )
        offset_max = 1 + int(self.offset_delta * offset_max)
        return random.randint(1, offset_max)

    def make_neuron(self):
        loop_list = [Segment(self.start, self.stop)]
        for _ in range(self.div_number):
            final_list = []
            for seg in loop_list:
                mid = seg.find_middle_point(self.find_offset(seg))
                s1, s2 = seg.split_segment(mid)
                final_list.append(s1)
                final_list.append(s2)
            loop_list = final_list.copy()
        self.segmentList = final_list

    def interpolate_neuron(self, sigma=2):
        temp_x = []
        temp_y = []
        for seg in self.segmentList:
            temp_y.append((seg.startPoint.y))
            temp_x.append((seg.startPoint.x))
        t = np.linspace(0, 1, len(temp_x), endpoint=True)
        t2 = np.linspace(0, 1, len(temp_y) + 20, endpoint=True)
        x2 = np.interp(t2, t, temp_x)
        y2 = np.interp(t2, t, temp_y)
        x3 = gaussian_filter1d(x2, sigma)
        y3 = gaussian_filter1d(y2, sigma)
        self.segmentList = []

        for i in range(len(x3[:-1])):
            start = Point(x3[i], y3[i])
            stop = Point(x3[i + 1], y3[i + 1])
            self.segmentList.append(Segment(start, stop))
