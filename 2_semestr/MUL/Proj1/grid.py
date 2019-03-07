import cv2
import numpy as np

from tools import *
from entity import Entity

class Grid():
    """
    class implements frame functionality
    """
    def __init__(self, original):
        self.original = original
        self.gray = gray(self.original)
        self.gray_blurred = blur(self.gray)
        self.width = np.size(original, 1)
        self.height = np.size(original, 0)
        self.blocks = []
        self.diff = []
        self.motion = []
        self.indexes = [21, 20, 17, 16,  5,  4,  1,  0,
                        22, 23, 18, 19,  6,  7,  2,  3,
                        25, 24, 29, 28,  9,  8, 13, 12,
                        26, 27, 30, 31, 10, 11, 14, 15,
                        37, 36, 33, 32, 53, 52, 49, 48,
                        38, 39, 34, 35, 54, 55, 50, 51,
                        41, 40, 45, 44, 57, 56, 61, 60,
                        42, 43, 46, 47, 58, 59, 62, 63]
        self.threshold = 20

        for x in range(0,64):
            self.blocks.append(None)
            self.diff.append(0)
            self.motion.append(False)

        index = 0
        for i, item in enumerate(four_quadrants(self.gray_blurred)):
            for e, elem in enumerate(four_quadrants(item)):
                for u, utem in enumerate(four_quadrants(elem)):
                    self.blocks[self.indexes.index(index)] = utem
                    index += 1

        self.p_width = int(self.width / 8)
        self.p_height = int(self.height / 8)


    def draw(self, last):
        """
        method finds moving objects and draw rectangles around them
        """
        x = int(self.p_width / 2)
        y = int(self.p_height / 2)

        for i, item in enumerate(self.blocks):
            err = mse(self.blocks[i], last.blocks[i])
            self.diff[i] = err

            if err > self.threshold:
                fontColor = (255,0,0)
                self.motion[i] = True
            else:
                fontColor = (255,255,255)
                self.motion[i] = False

            """
            if (i % 8) == 0 and i != 0:
                x = int(self.p_width / 2)
                y += self.p_height
            elif i != 0:
                x += self.p_width

            font      = cv2.FONT_HERSHEY_SIMPLEX
            coords    = (x, y)
            fontScale = 0.3
            lineType  = 2

            cv2.putText(self.original, str(round(err, 2)), 
                        coords, font, fontScale, fontColor, lineType)
            """

        objs = self.find_objects()
        for i, item in enumerate(objs):
            cv2.rectangle(self.original, (item.x1, item.y1), (item.x2, item.y2), (0,255,0), 2)

        return len(objs)


    def get_coords(self, index):
        """
        method returns coordinates of block with certain index
        """
        x1 = (index-(8*(index//8)))*self.p_width
        y1 = (index//8)*self.p_height
        x2 = x1 + self.p_width
        y2 = y1 + self.p_height

        return x1, y1, x2, y2


    def find_objects(self):
        """
        method finds block entities
        """
        used = set()
        entities = []

        for i, item in enumerate(self.motion):
            if self.motion[i] == True and i not in used:
                entity = Entity(self, i)
                used = used.union(set(entity.used))
                entities.append(entity)
            else:
                used.add(i)
        return entities
