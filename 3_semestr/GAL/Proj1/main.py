from collections import deque
import random

from graph import Graph
from graphs import g_1, g_2, g_3, g_4
from utils import draw_graph

def isPlanar(graph):
    V_count = len(graph.get_vertices())
    E_count = len(graph.get_edges())

    if E_count > 3 * V_count - 6:
        return False

    return True

def get_disconnected_components(graph):
    vertices = set(graph.get_vertices())
    components = []
    while vertices:
        s = random.choice(list(vertices))

        d = set()
        color = dict()
        
        for i, item in enumerate(list(vertices)):
            color[item] = "white"

        color[s] = "gray"
        Q = deque()
        Q.append(s)
        
        while Q:
            u = Q.popleft() 
            for _, v in enumerate(graph.get_Adj(u)):
                if color[v] == "white":
                    color[v] = "gray"
                    Q.append(v)
            color[u] = "black"
            d.add(u)

        components.append(d)
        vertices = vertices - d

    graphs = []
    for comp in components:
        graphs.append(Graph(dict((k, graph.get_graph_dict()[k]) for k in list(comp) if k in graph.get_graph_dict())))

    return graphs

def DFS(graph):
    def cycle(u):
        global DF_count
        DF_count += 1
        D[u] = DF_count
        for _, v in enumerate(graph.get_Adj(u)):
            if D[v] == 0:
                a[v] = u
                cycle(v)

    global DF_count
    DF_count = 0
    D = dict()
    a = dict()
    for i, item in enumerate(graph.get_vertices()):
        D[item] = 0
    
    u = random.choice(list(graph.get_vertices()))

    cycle(u)
    print(D)
    print(a)


if __name__ == "__main__":


    planar = Graph(g_1)
    non_planar = Graph(g_2)
    more_components = Graph(g_3)
    self_loop = Graph(g_4)

    planar.remove_self_loops()
    planar.remove_vertexes_of_degree_1()
    graphs = get_disconnected_components(planar) # get disconnected components

    for i, item in enumerate(graphs):
        print(item)

    DFS(planar)
