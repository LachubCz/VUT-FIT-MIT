from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

array = [ line for line in open('generated_spheres.txt')]

x_ = []
y_ = []
z_ = []
r_ = []

for i, item in enumerate(array):
    x_.append(float(item.split(" ")[0]))
    y_.append(float(item.split(" ")[1]))
    z_.append(float(item.split(" ")[2]))
    r_.append(float(item.split(" ")[3]))

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

for i in range(len(x_)):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = r_[i] * np.cos(u)*np.sin(v)
    y = r_[i] * np.sin(u)*np.sin(v)
    z = r_[i] * np.cos(v)
    ax.plot_wireframe(x+x_[i], y+y_[i], z+z_[i], color="r")


# draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

#a = Arrow3D([0, 1], [0, 1], [0, 1], mutation_scale=20,
#            lw=1, arrowstyle="-|>", color="k")
#ax.add_artist(a)
plt.show()