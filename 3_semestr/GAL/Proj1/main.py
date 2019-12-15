import random
random.seed(0)
from collections import deque
from operator import itemgetter

from graph import Graph
from utils import draw_graph
#from graphs import g_1, g_2, g_3, g_4

def isPlanar(graph):
    V_count = len(graph.get_vertices())
    E_count = len(graph.get_edges())

    if E_count > 3 * V_count - 6:
        return False

    if V_count < 5:
        return True

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
    def recursion(u):
        global DF_count
        DF_count += 1
        D[u] = DF_count
        children = 0
        low[u] = DF_count
        
        for i, v in enumerate(graph.get_Adj(u)):
            if D[v] == 0:
                a[v] = u
                children += 1
                recursion(v)
                low[u] = min(low[u], low[v]) 
                if a[u] == None and children > 1: 
                    ap[u] = True

                if a[u] != None and low[v] >= D[u]: 
                    ap[u] = True 

            elif v != a[u]:
                low[u] = min(low[u], D[v])

    global DF_count
    DF_count = 0

    D        = dict()
    a        = dict()
    low      = dict()
    ap       = dict()
    for i, item in enumerate(graph.get_vertices()):
        D[item] = 0
        a[item] = None
        low[item] = float("Inf")
        ap[item] = False
    
    u = random.choice(list(graph.get_vertices()))
    recursion(u)

    print("Order: {}" .format(D))
    print("Parents: {}" .format(a))
    print("Articulation points: {}" .format(ap))
    print("Lowpoints: {}" .format(low))

    order = dict((v,k) for k,v in D.items()) #swap keys with values

    L1 = dict()
    L2 = dict()
    L2_help = dict()
    for i in reversed(range(1, len(order)+1)):
        if order[i] != u:
            parent = a[order[i]]
        else:
            parent = None

        Adjs = graph.get_Adj(order[i])

        Adjs = Adjs.difference({parent})

        if len(Adjs) != 1:
            back = list(itemgetter(*frozenset(Adjs))(D))
        else:
            back = [D[list(Adjs)[0]]]
        back.append(i)

        if order[i] in L1:
            back.append(L1[order[i]])

        L1[order[i]] = min(set(back))
        if order[i] in L2_help:
            back = back + L2_help[order[i]]
        if order[i] != u:
            L2_help[a[order[i]]] = back

        back = set(back).difference({L1[order[i]]})
        L2[order[i]] = min(back)

        if order[i] != u:
            L1[a[order[i]]] = L1[order[i]]
        else:
            L2[order[i]] = D[order[2]]

    print("Lowpoints: {}" .format(L1))
    print("Lowpoints: {}" .format(L2))

    print(get_biconnected_components(graph, ap))

def get_biconnected_components(graph, ap):
    graph_dict = graph.get_graph_dict()
    for i, item in enumerate(ap.keys()):
        if ap[item]:
            del graph_dict[item]

    components = []
    vertices = set(graph.get_vertices())

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
                if v in graph_dict:
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


if __name__ == "__main__":
    #g = {"a" : {"f", "h", "b"},
    #     "b" : {"c", "a", "g"},
    #     "c" : {"h", "b", "d"},
    #     "h" : {"a", "c", "e"},
    #     "e" : {"d", "h", "f"},
    #     "f" : {"e", "g", "a"},
    #     "g" : {"b", "d", "f"},
    #     "d" : {"g", "e", "c"}
    #    }
    
    g = {"a" : {"b", "d"}, 
         "b" : {"a", "c"}, 
         "c" : {"b", "d", "e", "f"}, 
         "d" : {"a", "c"}, 
         "e" : {"c", "f"}, 
         "f" : {"c", "e"}
        }

    graph = Graph(g)

    #print(graph)
    #graph.symetrize()
    #print(graph)

    #graph.remove_self_loops()
    #graph.remove_vertexes_of_degree_1()
    #graphs = get_disconnected_components(graph)

    #for i, item in enumerate(graphs):
    #    print(item)

    #DFS2(graph)
    DFS(graph)
    #GetArticulationPoints(graph)