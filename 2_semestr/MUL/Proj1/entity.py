import numpy as np

from tools import *

class Entity():
    """
    class implements moving object
    """
    def __init__(self, frame, index):
        self.parts = list()
        self.parts.append(index)
        self.used = list()

        count = len(self.parts)
        e = 0
        while True:
            temp = get_neighbors(self.parts[e])
            for i, item in enumerate(temp):
                if item not in self.parts and frame.motion[item]:
                    self.parts.append(item)
                if item not in self.used:
                    self.used.append(item)

            e += 1
            if e == len(self.parts):
                break

        sorted_parts = sorted(self.parts)

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        #x1
        for i in range(0,8):
            divisible = divisible_numbers(self.parts, [8], i)
            if divisible != []:
                x1, _, x2, _ = frame.get_coords(divisible[0])
                break
        self.x1 = x1

        #y1
        _, y1, _, y2 = frame.get_coords(sorted_parts[0])
        self.y1 = y1

        #x2
        for i in reversed(range(0,8)):
            divisible = divisible_numbers(self.parts, [8], i)
            if divisible != []:
                x1, _, x2, _ = frame.get_coords(divisible[0])
                break
        self.x2 = x2

        #y2
        _, y1, _, y2 = frame.get_coords(sorted_parts[-1])
        self.y2 = y2
