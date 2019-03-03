import matplotlib.pyplot as plt
import numpy as np
import cv2
from timeit import default_timer as timer

def four_quadrants(image):
    """
    second | first
    -------+-------
    third  | fourth
    """
    width = np.size(image, 0)
    height = np.size(image, 1)

    half_width = int(width / 2)
    half_height = int(height / 2)

    first = image[0:half_width, half_height:height]
    second = image[0:half_width, 0:half_height]
    third = image[half_width:width, 0:half_height]
    fourth = image[half_width:width, half_height:height]

    return [first, second, third, fourth]


def mse(imageA, imageB):
    diff = (imageA.astype("float") - imageB.astype("float")) ** 2
    err = np.sum(diff)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err


def resize(image, size):
    return cv2.resize(image, (size, size))


def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur(image):
    return cv2.GaussianBlur(image, (21, 21), 0)


def put_text(frame, last):
    x = int(frame.p_width / 2)
    y = int(frame.p_height / 2)

    for i, item in enumerate(frame.blocks):
        if (i % 8) == 0 and i != 0:
            x = int(frame.p_width / 2)
            y += frame.p_height
        elif i != 0:
            x += frame.p_width

        err = mse(frame.blocks[i], last.blocks[i])
        frame[i].diff = err

        font      = cv2.FONT_HERSHEY_SIMPLEX
        coords    = (x, y)
        fontScale = 0.3
        if err > frame.threshold:
            fontColor = (255,0,0)
            frame[i].motion = True
        else:
            fontColor = (255,255,255)
            frame[i].motion = False
        lineType  = 2

        cv2.putText(frame.original, str(round(err, 2)), 
                    coords, font, fontScale, fontColor, lineType)
    #cv2.rectangle(frame.original, (30, 30), (60, 60), (255,0,0), 2)
    #cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)


def find_objects(frame):
    used = []
    for i, item in enumerate(frame.blocks):
        frame.blocks[i] = 0



class Object():
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0


class Grid():
    def __init__(self, original):
        self.original = original
        self.small = original#resize(self.original, 512)
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
            self.diff.append(False)

        index = 0
        for i, item in enumerate(four_quadrants(self.small_gray_blurred)):
            for e, elem in enumerate(four_quadrants(item)):
                for u, utem in enumerate(four_quadrants(elem)):
                    self.blocks[self.indexes.index(index)] = utem
                    index += 1
        self.p_width = int(self.width / 8)
        self.p_height = int(self.height / 8)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # Capture frame-by-frame
    ret, frame = cap.read()

    last = Grid(frame)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        frame = Grid(frame)

        # Draw operation
        start_time = timer()
        put_text(frame, last)
        end_time = timer() - start_time
        print("mse: " + str(end_time))
        # Display the resulting frame
        cv2.imshow('frame',frame.original)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        last = frame

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
