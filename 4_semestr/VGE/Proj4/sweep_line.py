import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from ear_clipping import fig2img


def print_triangle(ax, triangle, color, lines=False):
    polygon = Polygon(triangle, color=color, zorder=1)
    ax.add_patch(polygon)

    if lines:
        tri = triangle.transpose()

        plt.plot([tri[0,0], tri[0,1]], [tri[1,0], tri[1,1]], c='deeppink', zorder=2)
        plt.plot([tri[0,0], tri[0,2]], [tri[1,0], tri[1,2]], c='deeppink', zorder=2)
        plt.plot([tri[0,1], tri[0,2]], [tri[1,1], tri[1,2]], c='deeppink', zorder=2)


def get_sl_steps(coords, trap_edges, partition, triangles):
    steps = []
    for i in range(len(trap_edges)+1):
        fig, ax = plt.subplots(facecolor=(49/255, 52/255, 49/255))

        min_x = np.min(coords[:, 0])
        min_y = np.min(coords[:, 1])
        max_x = np.max(coords[:, 0])
        max_y = np.max(coords[:, 1])

        size_x = max_x - min_x
        size_y = max_y - min_y

        addon = np.max([size_x, size_y])/10

        polygon = Polygon(coords, color='darkgray', zorder=1)
        ax.add_patch(polygon)

        for e in range(i):
            print_triangle(ax, trap_edges[e], 'dimgray')

        plt.xlim(min_x - addon, max_x + addon)
        plt.ylim(min_y - addon, max_y + addon)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)

        ax.scatter(coords[:, 0], coords[:, 1], c='deeppink', zorder=3)

        img = fig2img(fig)
        steps.append(img)


    for i in range(1, len(partition)+1):
        fig, ax = plt.subplots(facecolor=(49/255, 52/255, 49/255))

        min_x = np.min(coords[:, 0])
        min_y = np.min(coords[:, 1])
        max_x = np.max(coords[:, 0])
        max_y = np.max(coords[:, 1])

        size_x = max_x - min_x
        size_y = max_y - min_y

        addon = np.max([size_x, size_y])/10

        polygon = Polygon(coords, color='darkgray', zorder=1)
        ax.add_patch(polygon)

        for e in range(len(trap_edges)):
            print_triangle(ax, trap_edges[e], 'dimgray')

        for e in range(i):
            print_triangle(ax, partition[e], 'blue')

        plt.xlim(min_x - addon, max_x + addon)
        plt.ylim(min_y - addon, max_y + addon)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)

        ax.scatter(coords[:, 0], coords[:, 1], c='deeppink', zorder=3)

        img = fig2img(fig)
        steps.append(img)


    for i in range(1, len(triangles)+1):
        fig, ax = plt.subplots(facecolor=(49/255, 52/255, 49/255))

        min_x = np.min(coords[:, 0])
        min_y = np.min(coords[:, 1])
        max_x = np.max(coords[:, 0])
        max_y = np.max(coords[:, 1])

        size_x = max_x - min_x
        size_y = max_y - min_y

        addon = np.max([size_x, size_y])/10

        polygon = Polygon(coords, color='darkgray', zorder=1)
        ax.add_patch(polygon)

        for e in range(len(trap_edges)):
            print_triangle(ax, trap_edges[e], 'dimgray')

        for e in range(len(partition)):
            print_triangle(ax, partition[e], 'blue')

        for e in range(i):
            print_triangle(ax, triangles[e], 'dimgray', True)

        plt.xlim(min_x - addon, max_x + addon)
        plt.ylim(min_y - addon, max_y + addon)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)

        ax.scatter(coords[:, 0], coords[:, 1], c='deeppink', zorder=3)

        img = fig2img(fig)
        steps.append(img)

    return steps


def parse_data(data):
    polygon = None
    trap_edges = []
    partition = []
    triangles = []

    for _, item in enumerate(data):
        if 'Polygon' in item:
            item = item[8:]
            item = item.replace('[', '')
            item = item.replace(']', '')
            item = item.replace('(', '')
            item = item.replace(' ', '')
            item = item.split(')')
            item = item[:-1]
            for e, elem in enumerate(item):
                item[e] = elem.split(',')
                for i in range(len(item[e])):
                    if item[e][i] == '':
                        del item[e][i]
                        break
                item[e] = list(map(int, item[e]))
            polygon = item

        elif 'TrapEdges' in item:
            item = item[10:]
            item = item.replace('(', '')
            item = item[:-1]
            item = item.split(') ')
            for e, elem in enumerate(item):
                elem = elem.replace(')', '')
                item[e] = elem.split(', ')
                item[e] = list(map(int, item[e]))
            trap_edges.append(item)

        elif 'Partition' in item:
            item = item[10:]
            item = item.replace('(', '')
            item = item[:-1]
            item = item.split(') ')
            for e, elem in enumerate(item):
                elem = elem.replace(')', '')
                item[e] = elem.split(', ')
                item[e] = list(map(int, item[e]))
            partition.append(item)

        elif 'listOfTriangles' in item:
            item = item[17:]
            item = item.replace('[', '')
            item = item[:-1]
            item = item.split('] ')
            for e, elem in enumerate(item):
                elem = elem.replace(']', '')
                item[e] = elem.split(', ')
                item[e] = list(map(float, item[e]))
                item[e] = list(map(int, item[e]))
            triangles.append(item)

    polygon = np.array(polygon)
    trap_edges = np.array(trap_edges)
    partition = np.array(partition)
    triangles = np.array(triangles)

    trap_edges_sort_index = np.argsort(np.min(trap_edges[:,:,1], axis=1))
    trap_edges_list = []
    for i, item in enumerate(trap_edges_sort_index):
        if trap_edges[item][0][0] == trap_edges[item][1][0] and trap_edges[item][0][1] == trap_edges[item][1][1]:
            pass
        else:
            trap_edges_list.append(trap_edges[item])

    trap_edges = np.array(trap_edges_list)

    triangles_final = []
    for i in range(0, len(triangles), 3):
        tria_set = set()
        tria_set.add(tuple(triangles[i][0]))
        tria_set.add(tuple(triangles[i][1]))
        tria_set.add(tuple(triangles[i+1][0]))
        tria_set.add(tuple(triangles[i+1][1]))
        tria_set.add(tuple(triangles[i+2][0]))
        tria_set.add(tuple(triangles[i+2][1]))

        triangles_final.append(list(tria_set))

    triangles = np.array(triangles_final)

    return polygon, trap_edges, partition, triangles
