import numpy as np

from tools import *

class Entity():
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
        print(sorted_parts)

        #x1
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        border_x1 = True
        for i in range(0,8):
            divisible = divisible_numbers(sorted_parts, [8], i)
            if divisible != []:
                x1 = divisible[0]
                break
            border_x1 = False
        #y1
        print(sorted_parts)
        y1 = sorted_parts[0]
        print(y1)
        #x2
        border_x2 = True
        for i in reversed(range(0,8)):
            divisible = divisible_numbers(sorted_parts, [8], i)
            if divisible != []:
                x2 = divisible[-1]
                break
            border_x2 = False
        #y2
        y2 = sorted_parts[-1]
        print(x1, y1, x2, y2)
        inner_1, inner_2, left, right, up, down = frame.get_borders(x1, y1, x2, y2, border_x1, border_x2)
        print(inner_1, inner_2, left, right, up, down)
        x1, y1, x2, y2 = frame.get_coords(inner_1)
        self.x1 = int((x1 * left) + ((1 - left) * x2))
        self.y1 = int((y1 * up) + ((1 - up) * y2))

        x1, y1, x2, y2 = frame.get_coords(inner_2)
        self.x2 = int((x1 * right) + ((1 - right) * x2))
        self.y2 = int((y1 * down) + ((1 - down) * y2))

        """
        #x1
        border = True
        for i in range(0,8):
            divisible = divisible_numbers(self.parts, [8], i)
            if divisible != []:
                x1, _, x2, _ = frame.get_coords(divisible[0])
                break
            border = False
        if border:
            self.x1 = x1
        else:
            self.x1 = int((x1 + x2) / 2)
        #y1
        _, y1, _, y2 = frame.get_coords(sorted_parts[0])
        if int(sorted_parts[0] / 8) == 0:
            self.y1 = y1
        else:
            self.y1 = int((y1 + y2) / 2)
        #x2
        border = True
        for i in reversed(range(0,8)):
            divisible = divisible_numbers(self.parts, [8], i)
            if divisible != []:
                x1, _, x2, _ = frame.get_coords(divisible[0])
                break
            border = False
        if border:
            self.x2 = x2
        else:
            self.x2 = int((x1 + x2) / 2)
        #y2
        _, y1, _, y2 = frame.get_coords(sorted_parts[-1])
        if int(sorted_parts[-1] / 8) == 7:
            self.y2 = y2
        else:
            self.y2 = int((y1 + y2) / 2)
        """