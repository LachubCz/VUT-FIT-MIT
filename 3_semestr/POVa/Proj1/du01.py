# coding: utf-8
from __future__ import print_function

import numpy as np
import cv2

# This should help with the assignment:
# * Indexing numpy arrays http://scipy-cookbook.readthedocs.io/items/Indexing.html


def parseArguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', help='Input video file name.')
    parser.add_argument('-i', '--image', help='Input image file name.')
    args = parser.parse_args()
    return args


def image(imageFileName):
    # read image
    img = cv2.imread(imageFileName)
    if img is None:
        print("Error: Unable to read image file", imageFileName)
        exit(-1)
    
    # print image width, height, and channel count
    print("Image dimensions: {}, {}, {}" .format(np.shape(img)[1], np.shape(img)[0], np.shape(img)[2]))
    
    # Resize to width 400 and height 500 with bicubic interpolation.
    img = cv2.resize(img, (400, 500), interpolation=cv2.INTER_CUBIC)
          
    # Print mean image color and standard deviation of each color channel
    print('Image mean and standard deviation: {}, {}; {}, {}; {}, {}'
          .format(round(np.mean(img[:,:,0].flatten()), 2), round(np.std(img[:,:,0].flatten()), 2),
                  round(np.mean(img[:,:,1].flatten()), 2), round(np.std(img[:,:,1].flatten()), 2),
                  round(np.mean(img[:,:,2].flatten()), 2), round(np.std(img[:,:,2].flatten()), 2)))
    
    # Fill horizontal rectangle with color 128.  
    # Position x1=50,y1=120 and size width=200, height=50
    rect = img.copy()
    rect = cv2.rectangle(rect, (50, 120), (250, 170), (128, 128, 128), cv2.FILLED)
    # write result to file
    cv2.imwrite('rectangle.png', rect)
    
    # Fill every third column in the top half of the image black.
    # The first column sould be black.  
    # The rectangle should not be visible.
    striped = img.copy()
    for i in range(int(np.shape(img)[0]/2)):
            for e in range(int(np.shape(img)[1])):
                if (e % 3) == 0:
                    striped[i,e,:] = 0
    # write result to file
    cv2.imwrite('striped.png', striped)
    
    # Set all pixels with any collor lower than 100 black.
    for i in range(np.shape(img)[0]):
        for e in range(np.shape(img)[1]):
            for u in range(np.shape(img)[2]):
                if img[i,e,u] < 100:
                    img[i,e,u] = 0
    
    #write result to file
    cv2.imwrite('clip.png', img)
   
    
def video(videoFileName):
    # open video file and get basic information
    videoCapture = cv2.VideoCapture(videoFileName)    
    frameRate = videoCapture.get(cv2.CAP_PROP_FPS)
    frame_width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not videoCapture.isOpened():
        print("Error: Unable to open video file for reading", videoFileName)
        exit(-1)
    
    # open video file for writing
    videoWriter  = cv2.VideoWriter(
        'videoOut.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 
        frameRate, (frame_width, frame_height))        
    if not videoWriter.isOpened():
        print("Error: Unable to open video file for writing", videoFileName)
        exit(-1)
                
    while videoCapture.isOpened():
        ret, frame = videoCapture.read()
        if not ret:
            break;
        
        # Flip image upside down.
        frame = cv2.flip(frame, 0)
                
        # Add white noise (normal distribution).
        # Standard deviation should be 5.
        noise = (np.random.normal(0, 5, size=(frame.shape))).astype(int)
        frame = frame + noise

        # Add gamma correction.
        # y = x^1.2 -- the image to the power of 1.2
        frame = (frame ** 1.2).astype(int)

        # Dim blue color to half intensity.
        for i in range(np.shape(frame)[0]):
            for e in range(np.shape(frame)[1]):
                frame[i,e,0] = int(frame[i,e,0] / 2)

        # Invert colors.
        frame = (255-frame)

        # Display the processed frame.         
        cv2.imshow("Output", frame.astype("uint8"))
        # Write the resulting frame to video file.
        videoWriter.write(frame)   
            
        # End the processing on pressing Escape.
        key = cv2.waitKey(10)
        if key == 27:
            break
        
    cv2.destroyAllWindows()        
    videoCapture.release()
    videoWriter.release()          
    

def main():
    args = parseArguments()
    np.random.seed(1)
    image(args.image)
    video(args.video)

if __name__ == "__main__":
    main()
