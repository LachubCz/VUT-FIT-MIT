from collections import deque
import random
random.seed(0)

from graph import Graph
#from graphs import g_1, g_2, g_3, g_4
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

from operator import itemgetter

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

    print(D, a)

    order = dict((v,k) for k,v in D.items()) #swap keys with values

    L1 = dict()
    L2 = dict()
    for i in reversed(range(1, len(order)+1)):
        if order[i] != u:
            parent = a[order[i]]
        else:
            parent = None

        Adjs = graph.get_Adj(order[i])

        Adjs = Adjs.difference({parent})

        print(order[i], Adjs)
        back = list(itemgetter(*frozenset(Adjs))(D))
        back.append(i)

        if order[i] in L1:
            back.append(L1[order[i]])

        L1[order[i]] = min(back)
        if order[i] != u:
            L1[a[order[i]]] = L1[order[i]]

    print(L1)

def DFS2(graph):
    def cycle(v):
        global pocet
        global S
        pocet += 1
        d[v] = pocet
        S = S.union({v})
        low[v] = d[v]
        komp.append(v)

        for _, w in enumerate(graph.get_Adj(v)):
            if w not in S:
                p[w] = v
                cycle(w)
                low[v] = min([low[v], low[v]])
            else:
                low[v] = min([low[v], d[v]])
        if d[v] >= 2 and low[v] == d[p[v]]:
            while True:
                u = komp.pop()
                if u == v:
                    break

    global pocet
    global S
    pocet = 0
    d = dict()
    S = set()
    low = dict()
    p = dict()
    komp = deque()
    
    u = random.choice(list(graph.get_vertices()))

    cycle(u)
    print(d)
    print(p)
    print(low)

if __name__ == "__main__":
    g = {"a" : {"f", "h", "b"},
         "b" : {"c", "a", "g"},
         "c" : {"h", "b", "d"},
         "h" : {"a", "c", "e"},
         "e" : {"d", "h", "f"},
         "f" : {"e", "g", "a"},
         "g" : {"b", "d", "f"},
         "d" : {"g", "e", "c"}
        }
    graph = Graph(g)

    graph.remove_self_loops()
    graph.remove_vertexes_of_degree_1()
    graphs = get_disconnected_components(graph)

    #for i, item in enumerate(graphs):
    #    print(item)

    #DFS2(graph)
    DFS(graph)
