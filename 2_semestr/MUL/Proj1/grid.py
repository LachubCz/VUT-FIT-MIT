import cv2
import numpy as np

from tools import *
from entity import Entity

class Grid():
    """
    class implements frame functionality
    """
    def __init__(self, original, threshold, memory):
        self.original = original
        #self.gray = gray(self.original)
        self.gray_blurred = blur(self.original)

        kernel = np.array([[-1,0,1],
                           [-2,0,2],
                           [-1,0,1]])
        self.sobel = cv2.filter2D(self.original, -1, kernel)
        self.sobel_gray = gray(self.sobel)
        self.sobel_gray_blurred = blur(self.sobel_gray)

        self.width = np.size(original, 1)
        self.height = np.size(original, 0)
        self.blocks_basic = []
        self.blocks_sobel = []
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
        self.threshold = threshold
        self.memory = memory

        for x in range(0,64):
            self.blocks_basic.append(None)
            self.blocks_sobel.append(None)
            self.diff.append(0)
            self.motion.append(False)

        index = 0
        for i, item in enumerate(four_quadrants(self.gray_blurred)):
            for e, elem in enumerate(four_quadrants(item)):
                for u, utem in enumerate(four_quadrants(elem)):
                    self.blocks_basic[self.indexes.index(index)] = utem
                    index += 1

        index = 0
        for i, item in enumerate(four_quadrants(self.sobel_gray_blurred)):
            for e, elem in enumerate(four_quadrants(item)):
                for u, utem in enumerate(four_quadrants(elem)):
                    self.blocks_sobel[self.indexes.index(index)] = utem
                    index += 1

        self.p_width = int(self.width / 8)
        self.p_height = int(self.height / 8)


    def draw(self, last):
        """
        method finds moving objects and draw rectangles around them
        """
        x = int(self.p_width / 2)
        y = int(self.p_height / 2)
        
        final = []
        for x in range(0,64):
            final.append(0)

        for i, item in enumerate(self.blocks_basic):
            err_basic = mse(self.blocks_basic[i], last.blocks_basic[i])
            err_sobel = mse(self.blocks_sobel[i], last.blocks_sobel[i])
            err = err_basic * 0 + err_sobel * 1
            self.diff[i] = err

            if len(self.memory) == 10:
                final[i] += self.memory[0][i] * 0.01
                final[i] += self.memory[1][i] * 0.02
                final[i] += self.memory[2][i] * 0.03
                final[i] += self.memory[3][i] * 0.04
                final[i] += self.memory[4][i] * 0.045
                final[i] += self.memory[5][i] * 0.05
                final[i] += self.memory[6][i] * 0.055
                final[i] += self.memory[7][i] * 0.07
                final[i] += self.memory[8][i] * 0.08
                final[i] += self.memory[9][i] * 0.1
                final[i] *= 0
                final[i] += self.diff[i] * 1
            else:
                final[i] = self.diff[i]

            if final[i] > self.threshold:
                fontColor = (255,0,0)
                self.motion[i] = True
            else:
                fontColor = (255,255,255)
                self.motion[i] = False
            
            if (i % 8) == 0 and i != 0:
                x = int(self.p_width / 2)
                y += self.p_height
            elif i != 0:
                x += self.p_width
            """
            font      = cv2.FONT_HERSHEY_SIMPLEX
            coords    = (x, y)
            fontScale = 0.3
            lineType  = 2

            cv2.putText(self.original, str(round(final[i], 2)), 
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
