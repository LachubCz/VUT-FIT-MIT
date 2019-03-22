import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

class ReactionTimeDistribuion():
    def __init__(self):
        x = np.array([100, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280,
                      300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500])
        y = np.array([0, 8, 60, 100, 200, 600, 10000, 25000, 40000, 55000, 60000, 50000, 40000,
                      33000, 26000, 20000, 15000, 11000, 9000, 7500, 6200, 4800, 0])
        arr = np.arange(np.amin(x), np.amax(x), 0.01)
        self.distribution = interpolate.CubicSpline(x, y)


    def get_prob(self):
        while True:
            x = 100+(500-100)*np.random.rand(1,1)[0][0]
            y = 60344*np.random.rand(1,1)[0][0]
            if self.distribution(x) > y:
                return x


def exp_type(curr_expr, experiments):
    for i, item in enumerate(experiments):
        if item[0] and curr_expr!=i:
            return i

    return curr_expr


def get_graph():
    wewe = ReactionTimeDistribuion()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#313431")

    rx = np.arange(100, 500, 1)
    ry = np.zeros(400)
    for i in range(400):
        ry[i] = wewe.distribution(rx[i])

    lag = wewe.get_prob()
    plt.plot(rx, ry, "-r", color="white")
    plt.plot(lag, wewe.distribution(lag), 'ob', color=(117/255,191/255,255/255))

    ax.set_facecolor((31/255,34/255,31/255))
    ax.axis('off')

    fig.set_size_inches(3, 1)

    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    return img, lag


def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    """Overlay img_overlay on top of img at the position specified by
    pos and blend using alpha_mask.

    Alpha mask must contain values within the range [0, 1] and be the
    same size as img_overlay.
    """

    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                alpha_inv * img[y1:y2, x1:x2, c])