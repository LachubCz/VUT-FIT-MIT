import cv2
import numpy as np

from tools import *
from entity import Entity

class Grid():
    def __init__(self, original):
        self.original = original
        self.small = original
        self.small_gray = gray(self.small)
        self.small_gray_blurred = blur(self.small_gray)
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
        for i, item in enumerate(four_quadrants(self.small_gray_blurred)):
            for e, elem in enumerate(four_quadrants(item)):
                for u, utem in enumerate(four_quadrants(elem)):
                    self.blocks[self.indexes.index(index)] = utem
                    index += 1
        self.p_width = int(self.width / 8)
        self.p_height = int(self.height / 8)

    def put_text(self, last):
        x = int(self.p_width / 2)
        y = int(self.p_height / 2)

        for i, item in enumerate(self.blocks):
            
            if (i % 8) == 0 and i != 0:
                x = int(self.p_width / 2)
                y += self.p_height
            elif i != 0:
                x += self.p_width
            
            err = mse(self.blocks[i], last.blocks[i])
            self.diff[i] = err
            
            font      = cv2.FONT_HERSHEY_SIMPLEX
            coords    = (x, y)
            fontScale = 0.3
            
            if err > self.threshold:
                fontColor = (255,0,0)
                self.motion[i] = True
            else:
                fontColor = (255,255,255)
                self.motion[i] = False
            
            lineType  = 2

            cv2.putText(self.original, str(round(err, 2)), 
                        coords, font, fontScale, fontColor, lineType)
            #cv2.rectangle(self.original, (30, 30), (60, 60), (255,0,0), 2)
            #x1, y1, x2, y2 = get_coords(self, i)
            
        objs = self.find_objects()
        for i, item in enumerate(objs):
            cv2.rectangle(self.original, (item.x1, item.y1), (item.x2, item.y2), (0,255,0), 2)
        tm = create_timestamp()
        print(tm)
        #cv2.imwrite(tm+'.png',self.original)


    def get_coords(self, index):
        x1 = (index-(8*(index//8)))*self.p_width
        y1 = (index//8)*self.p_height
        x2 = x1 + self.p_width
        y2 = y1 + self.p_height

        return x1, y1, x2, y2


    def find_objects(self):
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


    def get_borders(self, x1, y1, x2, y2, border_x1, border_x2):
        """
        ___3__
        |     |
        1     2
        |__4__|
        """
        up = 0.5
        down = 0.5
        left = 0.5
        right = 0.5

        if x1 // 8 != y1 // 8:
            if (x1-(8*(x1//8))) < (y1-(8*(y1//8))):
                inner_1 = y1 - ((y1-(8*(y1//8))) - (x1-(8*(x1//8))))
            else:
                inner_1 = y1
        else:
            inner_1 = y1
        outer_1 = inner_1 - 9
        if x2 // 8 != y2 // 8:
            if (x2-(8*(x2//8))) > (y2-(8*(y2//8))):
                inner_2 = y2 + ((x2-(8*(x2//8)))-(y2-(8*(y2//8))))
            else:
                inner_2 = y2
        else:
            inner_2 = y2

        outer_2 = inner_2 + 9

        out_of_left = False
        out_of_right = False
        out_of_up = False
        out_of_down = False

        if border_x1:
            out_of_left = True
        if border_x2:
            out_of_right = True
        if (outer_1 // 8) == 0:
            out_of_up = True
        if outer_2 > 54:
            out_of_down = True

        width = (inner_2-(8*(inner_2//8))) - (inner_1-(8*(inner_1//8)))
        height = inner_2//8 - inner_1//8

        left_i = self.diff[inner_1]
        right_i = self.diff[inner_1]
        up_i = self.diff[inner_1]
        down_i = self.diff[inner_1]

        for i in range(height):
            if (inner_1+8) < 64:
                left_i += self.diff[inner_1+8]
            if (inner_2-8) > -1:
                right_i += self.diff[inner_2-8]

        for i in range(width):
            if 0 != (inner_1-(8*(inner_1//8))):
                up_i += self.diff[inner_1+1]
            if 7 != (inner_2-(8*(inner_2//8))):
                down_i += self.diff[inner_2-1]

        width = (outer_2-(8*(outer_2//8))) - (outer_1-(8*(outer_1//8)))
        height = outer_2//8 - outer_1//8

        left_o = self.diff[outer_1]
        right_o = self.diff[outer_1]
        up_o = self.diff[inner_1]
        down_o = self.diff[inner_1]

        for i in range(height):
            if not out_of_left:
                left_o += self.diff[outer_1+8]
            if not out_of_right:
                right_o += self.diff[outer_2-8]

        for i in range(width):
            if not out_of_up:
                up_o += self.diff[outer_1+1]
            if not out_of_down:
                down_o += self.diff[outer_2-1]

        left = left_o / (left_o + left_i) 
        right = right_o / (right_o + right_i)
        print()
        up = up_o / (up_o + up_i)
        down = down_o / (down_o + down_i)

        if border_x1:
            left = 1
        if border_x2:
            right = 0
        if y1 < 8:
            up = 1
        if y2 > 55:
            down = 0

        return inner_1, inner_2, left, right, up, down
