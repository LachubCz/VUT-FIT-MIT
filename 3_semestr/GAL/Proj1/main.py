from collections import deque
import random

from graph import Graph
from utils import draw_graph

def isPlanar(graph):
    V_count = len(graph.vertices())
    E_count = len(graph.edges())

    if E_count > 3 * V_count - 6:
        return False

    return True

def get_disconnected_components(graph):
    vertices = set(graph.vertices())
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
        graphs.append(Graph(dict((k, graph.graph_dict()[k]) for k in list(comp) if k in graph.graph_dict())))

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
    for i, item in enumerate(graph.vertices()):
        D[item] = 0
    
    u = random.choice(list(graph.vertices()))

    cycle(u)
    print(D)
    print(a)


if __name__ == "__main__":
    g_1 = {"a" : {"e", "b"},
           "b" : {"a", "e", "f", "c"},
           "c" : {"b", "g", "h"},
           "d" : {"e", "l"},
           "e" : {"a", "b", "i", "d"},
           "f" : {"b", "g"},
           "g" : {"c", "f", "j"},
           "h" : {"c", "k", "o"},
           "i" : {"e", "j", "l"},
           "j" : {"i", "g", "k"},
           "k" : {"j", "h", "o", "m"},
           "l" : {"d", "i", "m"},
           "m" : {"l", "k", "n"},
           "n" : {"m", "o"},
           "o" : {"h", "k", "n"}
          }

    g_2 = {"a" : {"e", "b"},
           "b" : {"a", "e", "f", "c"},
           "c" : {"b", "g", "h"},
           "d" : {"e", "l"},
           "e" : {"a", "b", "i", "d"},
           "f" : {"b", "g", "k"},
           "g" : {"c", "f", "j"},
           "h" : {"c", "k", "o"},
           "i" : {"e", "j", "l"},
           "j" : {"i", "g", "k"},
           "k" : {"j", "h", "o", "m", "f"},
           "l" : {"d", "i", "m"},
           "m" : {"l", "k", "n"},
           "n" : {"m", "o"},
           "o" : {"h", "k", "n"}
          }

    g_3 = {"a" : {"e", "b"},
           "b" : {"a", "e", "f", "c"},
           "c" : {"b", "g"},
           "d" : {"l"},
           "e" : {"a", "b"},
           "f" : {"b", "g"},
           "g" : {"c", "f"},
           "h" : {"k", "o"},
           "i" : {"j", "l"},
           "j" : {"i", "k"},
           "k" : {"j", "h", "o", "m"},
           "l" : {"d", "i", "m"},
           "m" : {"l", "k", "n"},
           "n" : {"m", "o"},
           "o" : {"h", "k", "n"}
          }

    g_4 = {"a" : {"b"},
           "b" : {"a", "c", "d"},
           "c" : {"b"},
           "d" : {"b", "d"},
           "e" : {}
          }

    planar = Graph(g_1)
    non_planar = Graph(g_2)
    more_components = Graph(g_3)
    self_loop = Graph(g_4)

    print(isPlanar(planar))
    print(isPlanar(non_planar))

                    #remove self loops
                    #remove vertexes of degree 1
    graphs = get_disconnected_components(planar) # get disconnected components

    for i, item in enumerate(graphs):
        print(item)

    print(self_loop)
    self_loop.remove_self_loops()
    print(self_loop)
    self_loop.remove_vertexes_of_degree_1()
    print(self_loop)
    graphs = get_disconnected_components(self_loop)
    for i, item in enumerate(graphs):
        print(item)

    print("####")
    DFS(planar)

    draw_graph(planar)