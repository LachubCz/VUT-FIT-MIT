import cv2
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from PIL import Image

import tripy

def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf


def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    pil_image = Image.frombytes("RGBA", (w, h), buf.tostring())
    opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return opencvImage


def print_triangle(ax, triangle):
    polygon = Polygon(triangle, color='dimgray', zorder=1)
    ax.add_patch(polygon)

    tri = triangle.transpose()

    plt.plot([tri[0,0], tri[0,1]], [tri[1,0], tri[1,1]], c='deeppink', zorder=2)
    plt.plot([tri[0,0], tri[0,2]], [tri[1,0], tri[1,2]], c='deeppink', zorder=2)
    plt.plot([tri[0,1], tri[0,2]], [tri[1,1], tri[1,2]], c='deeppink', zorder=2)


def get_ec_steps(coords):
    triangles = np.array(tripy.earclip(np.array(coords)))

    steps = []
    for i in range(len(triangles)+1):
        fig, ax = plt.subplots(facecolor=(49/255, 52/255, 49/255))

        # coordinates for empty space cropping
        min_x = np.min(coords[:, 0])
        min_y = np.min(coords[:, 1])
        max_x = np.max(coords[:, 0])
        max_y = np.max(coords[:, 1])

        size_x = max_x - min_x
        size_y = max_y - min_y

        addon = np.max([size_x, size_y])/10

        # create and plot polygon
        polygon = Polygon(coords, color='darkgray', zorder=1)
        ax.add_patch(polygon)

        for e in range(i):
            print_triangle(ax, triangles[e])

        # crop empty space around graph
        plt.xlim(min_x - addon, max_x + addon)
        plt.ylim(min_y - addon, max_y + addon)

        # don't show axes
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)

        # plot vertices
        ax.scatter(coords[:, 0], coords[:, 1], c='deeppink', zorder=3)

        img = fig2img(fig)
        steps.append(img)

    return steps

if __name__ == '__main__':
    # polygon coordinates
    coords = np.array(
        [[350, 75], [379, 161], [469, 161], [397, 215], [423, 301], [350, 250], [277, 301], [303, 215], [231, 161],
         [321, 161]])
    steps = get_ec_steps(coords)
