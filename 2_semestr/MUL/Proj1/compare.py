# USAGE
# python compare.py

# import the necessary packages
#from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
from timeit import default_timer as timer

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err


def four_quadrants(image):
    """
    second | first
    -------+-------
    third  | fourth
    """
    height, width = image.shape[:2]

    half_width = int(width / 2)
    half_height = int(height / 2)

    first = image[half_width:width, 0:half_height]
    second = image[0:half_width, 0:half_height]
    third = image[0:half_width, half_height:height]
    fourth = image[half_width:width, half_height:height]

    return first, second, third, fourth


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    start_time = timer()
    m = mse(imageA, imageB)
    end_time = timer() - start_time
    print("mse: " + str(end_time))
    
    #s = ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f" % (m))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()

if __name__ == '__main__':
    # load images
    original = cv2.imread("images/first.jpg")
    contrast = cv2.imread("images/same.jpg")
    shopped = cv2.imread("images/diffrent.jpg")


    #compare_images(original, contrast, "Original vs. Original")
    # convert images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)

    # resize
    original = cv2.resize(original, (512, 512))
    contrast = cv2.resize(contrast, (512, 512))
    shopped = cv2.resize(shopped, (512, 512))
    # initialize the figure
    #fig = plt.figure("Images")
    #images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)

    # loop over the images
    #for (i, (name, image)) in enumerate(images):
        # show the image
    #    ax = fig.add_subplot(1, 3, i + 1)
    #    ax.set_title(name)
    #    plt.imshow(image, cmap = plt.cm.gray)
    #    plt.axis("off")

    # show the figure
    #plt.show()

    # compare the images
    """
    compare_images(original, original, "Original vs. Original")
    compare_images(original, contrast, "Original vs. Contrast")
    compare_images(original, shopped, "Original vs. Photoshopped")
    """

    first_o, second_o, third_o, fourth_o = four_quadrants(original)
    first_c, second_c, third_c, fourth_c = four_quadrants(contrast)
    first_s, second_s, third_s, fourth_s = four_quadrants(shopped)
    """
    compare_images(first_o, first_o, "Original vs. Original")
    compare_images(second_o, second_o, "Original vs. Contrast")
    compare_images(third_o, third_o, "Original vs. Photoshopped")
    compare_images(fourth_o, fourth_o, "Original vs. Photoshopped")

    compare_images(first_o, first_c, "Original vs. Original")
    compare_images(second_o, second_c, "Original vs. Contrast")
    compare_images(third_o, third_c, "Original vs. Photoshopped")
    compare_images(fourth_o, fourth_c, "Original vs. Photoshopped")

    compare_images(first_s, first_c, "Original vs. Original")
    compare_images(second_s, second_c, "Original vs. Contrast")
    compare_images(third_s, third_c, "Original vs. Photoshopped")
    compare_images(fourth_s, fourth_c, "Original vs. Photoshopped")
    """
    print(mse(first_o, first_c),mse(first_o, first_s))
    print(mse(second_o, second_c),mse(second_o, second_s))
    print(mse(third_o, third_c),mse(third_o, third_s))
    print(mse(fourth_o, fourth_c),mse(fourth_o, fourth_s))
