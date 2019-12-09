# coding: utf-8
from __future__ import print_function

import numpy as np
import cv2

def parseArguments():
    import argparse
    parser = argparse.ArgumentParser(
        epilog='Grab cut demonstration. ' +
        'Manually crop rectangle by mouse drag. ' +
        'An interactive Grab cut segmentation session is run on the selected crop. ' +
        'Label foreground and background pixels as needed with mouse. ' +
        'Use "f" and "b" keys to switch to foreground respective background annotation. ' +
        'Use "space" to update the segmentation. Exit by pressing Escape key.')
    parser.add_argument('-i', '--image', required=True,
                        help='Image file name.')
    args = parser.parse_args()
    return args


class rectangleCropCallback(object):
    def __init__(self):
        self.firstPoint = None
        self.secondPoint = None
        self.cropping_now = False
        self.finished_cropping = False

    def mouseCallback(self, event, x, y, flags, param):
        # If the left mouse button is clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed.
        if event == cv2.EVENT_LBUTTONDOWN:
            self.firstPoint = self.secondPoint =(int(x), int(y))
            self.cropping_now = True

        # If cropping, update rectangle.
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping_now == True:
                self.secondPoint = (int(x), int(y))

        # Finish cropping when left mouse button is released.
        elif event == cv2.EVENT_LBUTTONUP:
            if self.cropping_now == True:
                self.secondPoint = (int(x), int(y))
                self.cropping_now = False
                self.finished_cropping = True


class grabCutCallback(object):
    def __init__(self, image):
        self.img = image
        # Create inital foreground/background mask.
        # Lets say that all pixels probably contain background.
        # Grab cut starts from this mask and outputs results here as well.
        self.mask = np.full(
            shape=image.shape[:2], fill_value=cv2.GC_PR_BGD, dtype=np.uint8)
        self.annotating_foreground = True
        self.drawing_active = False

    def draw(self):
        img = self.img.copy()
        # Mark foreground in the image.
        img[:, :, 1][self.mask == cv2.GC_FGD] = 0
        img[:, :, 1][self.mask == cv2.GC_PR_FGD] = img[:, :, 1][self.mask == cv2.GC_PR_FGD] / 2
        # Mark background in the image.
        img[:, :, 2][self.mask == cv2.GC_BGD] = 0
        img[:, :, 2][self.mask == cv2.GC_PR_BGD] = img[:, :, 2][self.mask == cv2.GC_PR_BGD] / 2
        return img

    def mouseCallback(self, event, x, y, flags, param):
        # Start drawing into mask on mouse button press.
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing_active = True
            if self.annotating_foreground:
                self.mask[int(y), int(x)] = cv2.GC_FGD
            else:
                self.mask[int(y), int(x)] = cv2.GC_BGD

        # Draw mask pixels on mouse move.
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing_active:
                if self.annotating_foreground:
                    self.mask[int(y), int(x)] = cv2.GC_FGD
                else:
                    self.mask[int(y), int(x)] = cv2.GC_BGD

        # Stop drawing annotation on button release.
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing_active = False


def main():
    args = parseArguments()

    # Will be using two windows.
    # One for cropping. One for segmentation.
    cv2.namedWindow('image')
    cv2.namedWindow('segmentation', cv2.WINDOW_NORMAL)

    inputImage = cv2.imread(args.image)

    # Init callback for cropping.
    cropCB = rectangleCropCallback()
    # Assign the callback to 'image' window.
    # In python cropCB.mouseCallback is a bound function
    # - it rememberes the cropCB object and can be passed as anny other object.
    cv2.setMouseCallback('image', cropCB.mouseCallback)
    segmentCB = grabCutCallback(inputImage)

    while(True):
        # Create image copy as we will draw inside it.
        tmpImg = inputImage.copy()

        # If cropping in progress, draw the region.
        if cropCB.cropping_now:
            # Draw rectangle between cropCB.firstPoint and cropCB.secondPoint.
            # Use color (255, 0, 0). You can use cv2.rectangle().
            # Draw into tmpImg.
            tmpImg = cv2.rectangle(tmpImg, cropCB.firstPoint, cropCB.secondPoint, (255, 0, 0), cv2.FILLED)

        # Start segmentation when cropping done.
        if cropCB.finished_cropping:
            cropCB.finished_cropping = False

            # Get rectangular crop.
            x1 = min(cropCB.firstPoint[0], cropCB.secondPoint[0])
            y1 = min(cropCB.firstPoint[1], cropCB.secondPoint[1])
            width = abs(cropCB.secondPoint[0] - cropCB.firstPoint[0])
            height = abs(cropCB.secondPoint[1] - cropCB.firstPoint[1])
            crop = inputImage[y1:y1 + height, x1:x1 + width, :]

            segmentCB = grabCutCallback(crop)
            # Assign the callback to 'segmentation' window.
            cv2.setMouseCallback('segmentation', segmentCB.mouseCallback)
            

        # Draw current segmentation.
        if segmentCB:
            cv2.imshow('segmentation', segmentCB.draw())

        cv2.imshow('image', tmpImg)

        key = cv2.waitKey(20) & 0xFF
        if key == 27:
            break
        elif key == ord('f') and segmentCB:
            segmentCB.annotating_foreground = True
        elif key == ord('b') and segmentCB:
            segmentCB.annotating_foreground = False
        elif key == ord(' ') and segmentCB:
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            # Run cv2.grabCut() on segmentCB.img and segmentCB.mask.
            # Init with the current mask. Run 2 iterations.
            temp = segmentCB.img.copy()
            segmentCB.mask, bgdModel, fgdModel = cv2.grabCut(temp, segmentCB.mask, 
                            rect=(cropCB.firstPoint[0],cropCB.firstPoint[1],cropCB.secondPoint[0], cropCB.secondPoint[1]),
                                                   bgdModel=bgdModel, fgdModel=fgdModel, iterCount=5)
            

    if segmentCB:
        # Create binary mask where True/1 is assingled to cv2.GC_FGD and cv2.GC_PR_FGD.
        # cv2.cv2.GC_PR_BGD and cv2.GC_BGD are assigned False/0.
        # The source mask is in segmentCB.mask.
        mask = np.zeros(segmentCB.mask.shape)
        for i, item in enumerate(segmentCB.mask):
            for e, _ in enumerate(item):
                if segmentCB.mask[i][e] == cv2.GC_FGD or segmentCB.mask[i][e] == cv2.GC_PR_FGD:
                    mask[i][e] = 1
                elif segmentCB.mask[i][e] == cv2.GC_PR_BGD or segmentCB.mask[i][e] == cv2.GC_BGD:
                    mask[i][e] = 0

        # Adding some random foreground noise to mask.
        positions0 = np.random.random_integers(mask.shape[0] - 1, size=100)
        positions1 = np.random.random_integers(
            mask.shape[1] - 1, size=positions0.size)
        mask[positions0, positions1] = 1

        # Adding some random background noise to mask.
        positions0 = np.random.random_integers(mask.shape[0] - 1, size=100)
        positions1 = np.random.random_integers(
            mask.shape[1] - 1, size=positions0.size)
        mask[positions0, positions1] = 0

        mask = np.uint8(mask)
        cv2.imshow('noisy mask', mask * 255)

        # Remove lonely foreground pixels. Use morfological operation open -
        # erosion followed by dilatation. Use 'kernel'.
        kernel = np.ones((3, 3), dtype=np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1) 
        mask = cv2.dilate(mask, kernel, iterations=1)         

        # Remove small holes in foregound. Use morfological operation close -
        # dilatation followed by erosion. Use 'kernel'.
        mask = cv2.dilate(mask, kernel, iterations=1)    
        mask = cv2.erode(mask, kernel, iterations=1) 
        cv2.imshow('repaired mask', np.uint8(mask) * 255)

        # Mask foreground pixels. Set background to 0.
        # Use 'mask' and segmentCB.img
        maskedForeground = np.zeros((segmentCB.img.shape))
        for i, item in enumerate(maskedForeground):
            for e, _ in enumerate(item):
                if mask[i][e] == 1:
                    maskedForeground[i][e][0] = segmentCB.img[i][e][0]/255
                    maskedForeground[i][e][1] = segmentCB.img[i][e][1]/255
                    maskedForeground[i][e][2] = segmentCB.img[i][e][2]/255

        cv2.imshow('masked foreground', maskedForeground)

        # Distance transform - highlight pixels 20px distant from foreground
        distances = cv2.distanceTransform(1-mask, cv2.DIST_L2, 3)

        distances = np.uint32(distances) == 20
        cv2.imshow('distance 20', np.uint8(distances) * 255)
        cv2.waitKey()

        # Compute vertical and horizontal projection of the foreground.
        # Sum mask pixel in horizontal lines respective vertical columns.
        # Use matplotlib.pyplot to plot the projection graphs.
        # Use subplot() to put both graphs into a single window.
        import matplotlib.pyplot as plt
        horizontal = np.zeros((mask.shape[0]))
        vertical = np.zeros((mask.shape[1]))
        for i, item in enumerate(mask):
            for e, _ in enumerate(item):
                if mask[i][e] == 1:
                    vertical[e] += 1
                    horizontal[i] += 1
        
        vertical_x = np.arange(vertical.shape[0])
        horizontal_x = np.arange(horizontal.shape[0])
        money = vertical

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
        ax[0].bar(vertical_x, vertical)
        ax[1].bar(horizontal_x, horizontal)

        plt.show()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
