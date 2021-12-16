import random

from point import Point


class Segment:
    """Definition d'un segment"""

    def __init__(self, start, stop):
        self.startPoint = start
        self.endPoint = stop

    def find_middle_point(self, offset):
        mid_x = sum([self.startPoint.x, self.endPoint.x]) / 2
        mid_y = sum([self.startPoint.y, self.endPoint.y]) / 2
        offsetx = random.randint(-offset, offset)
        offsety = random.randint(-offset, offset)

        return Point(int(mid_x + offsetx), int(mid_y + offsety))

    def split_segment(self, mid):
        new_seg_1 = Segment(self.startPoint, mid)
        new_seg_2 = Segment(mid, self.endPoint)
        return new_seg_1, new_seg_2
