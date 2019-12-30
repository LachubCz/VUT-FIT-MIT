import argparse

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from matplotlib.collections import PatchCollection

import matplotlib.colors as colors


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-x", action="store", type=int, required=True)
    parser.add_argument("-y", action="store", type=int, required=True)
    parser.add_argument("-z", action="store", type=int, required=True)
    parser.add_argument("-r", action="store", type=int, required=True)

    args = parser.parse_args()

    return args


def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)

    return collection


if __name__ == '__main__':
    args = get_args()
    array = [ line for line in open('generated_spheres.txt')]

    x = []
    y = []
    z = []
    r = []

    for i, item in enumerate(array):
        x.append(float(item.split(" ")[0]))
        y.append(float(item.split(" ")[1]))
        z.append(float(item.split(" ")[2]))
        r.append(float(item.split(" ")[3]))

    x.append(args.x)
    y.append(args.y)
    z.append(args.z)
    r.append(args.r)

    colors_list = list(colors._colors_full_map.values())
    colors_=arange(len(x))

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")

    for i in range(len(x)):
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        coord_x = r[i] * np.cos(u)*np.sin(v)
        coord_y = r[i] * np.sin(u)*np.sin(v)
        coord_z = r[i] * np.cos(v)
        ax.plot_wireframe(coord_x+x[i], coord_y+y[i], coord_z+z[i], color=colors_list[i])

    plt.show()

    figure(figsize=(8,8))
    ax=subplot(aspect='equal')

    xlim(0,1000)
    ylim(0,1000)

    out_xy = circles(x, y, r, colors_, alpha=0.5, edgecolor='none')
    plt.show()

    figure(figsize=(8,8))
    ax=subplot(aspect='equal')

    xlim(0,1000)
    ylim(0,1000)

    out_xz = circles(x, z, r, colors_, alpha=0.5, edgecolor='none')
    plt.show()

    figure(figsize=(8,8))
    ax=subplot(aspect='equal')

    xlim(0,1000)
    ylim(0,1000)

    out_yz = circles(y, z, r, colors_, alpha=0.5, edgecolor='none')
    plt.show()
