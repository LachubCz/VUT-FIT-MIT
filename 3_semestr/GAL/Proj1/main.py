import random
random.seed(0)
from collections import deque
from operator import itemgetter

import numpy as np

from graph import Graph, OrderedGraph
from graphs import g_1, g_2, g_3, g_4, g_5, g_6

def isPlanar(graph):
    def isSegmentPlanar(vertexS, vertexT):
        aLefts =      [] #LinkedList<LinkedList<Integer>>
        aRights =     [] #LinkedList<LinkedList<Integer>>
        A =           [] #LinkedList<Integer>
        actAdjacent = [] #LinkedList<Integer>
        aMaxL =       [] #LinkedList<Integer>
        aMaxR =       [] #LinkedList<Integer>
        spine =       [] #LinkedList<Integer>

        source = vertexT;

        target = new_graph.get_Adj(vertexT)[0];
        if vertexT > vertexS:
            spine.append(vertexT)
            while target > source:
                spine.append(target)
                source = target
                target = new_graph.get_Adj(target)[0];

        while spine != []:
            source = spine[-1]
            del spine[-1]

            actAdjacent = new_graph.get_Adj(source)
            for i in range(1, len(actAdjacent)):
                target = actAdjacent[i]

                A = isSegmentStronglyPlanar(source, target)
                if A == False:
                    return False
                
                if target < source:
                    aMin = target
                else:
                    aMin = L1[order[target]]

                if not bipartity_test(aMin, A, aLefts, aRights):
                    return False

            previous = a[order[source]]
            stop = False
            while not stop:
                if not (aLefts == []) and previous >= 0:
                    aMaxL = aLefts[-1]
                    del aLefts[-1]
                    while not (aMaxL == []) and aMaxL[-1] == previous:
                        if len(aMaxL) > 0:
                            del aMaxL[-1]

                    aMaxR = aRights[-1]
                    del aRights[-1]
                    while not (aMaxR == []) and aMaxR[-1] == previous:
                        del aMaxR[-1]

                    if not (aMaxL == []) or not (aMaxR == []):
                        aLefts.append(aMaxL)
                        aRights.append(aMaxR)
                        stop = True
                else:
                    stop = True

        arb = [] # LinkedList<Integer>
        alb = [] # LinkedList<Integer>

        w1 = vertexT
        previous = vertexS
        while L1[order[vertexT]]:
            w1 = previous
            previous = a[order[previous]]

        while not (aLefts == []):
            arb = aRights[0]
            del aRights[0]

            alb = aLefts[0]
            del aLefts[0]

            if not (alb == []) and not (arb == []) and alb[-1] >= w1 and arb[-1] >= w1:
                return False

        return True

    graph.symetrize()
    graph.remove_self_loops()
    graph.remove_vertices_of_degree_1()
    graph_components = get_disconnected_components(graph)

    for _, component in enumerate(graph_components):
        V_count = len(graph.get_vertices())
        E_count = len(graph.get_edges())

        if E_count > 3 * V_count - 6:
            return False
        _, _, _, ap, _, _ = DFS(component, lowpoints=False)
        bicomponents = get_biconnected_components(component, ap)
        for _, bicomponent in enumerate(bicomponents):
            D, a, low, ap, L1, L2 = DFS(bicomponent)
            new_graph = OrderedGraph()
            for _, u in enumerate(bicomponent.get_vertices()):
                new_graph.add_vertex(D[u])
                Adjs = list(bicomponent.get_Adj(u))
                wt = []
                for _, v in enumerate(Adjs):
                    if a[v] != u:
                        if a[u] == v:    
                            wt.append(-1)
                        elif (D[u] > D[v]):
                            wt.append(2 * D[v])
                        else:
                            wt.append(-1)
                    elif a[v] == u and L2[v] >= D[u]:
                        wt.append(2 * L1[v])
                    elif a[v] == u and L2[v] < D[u]:
                        wt.append(2 * L1[v] + 1)
                order = np.argsort(wt)
                for i, item in enumerate(order):
                    if wt[item] != -1:
                        new_graph.add_edge((D[u], D[Adjs[item]]))
            V_count = len(bicomponent.get_vertices())
            if V_count >= 5:
                order = dict((v,k) for k,v in D.items())
                if not isSegmentPlanar(0, 1):
                    return False

    return True


def bipartity_test(minimum, A, aLefts, aRights): #int, LinkedList<Integer>, LinkedList<LinkedList<Integer>>, LinkedList<LinkedList<Integer>>
    i = len(aLefts)
    if i == 0:
        aLefts.append(A)
        aRights.append([])
        return True

    aL = [] #LinkedList<Integer>
    aR = [] #LinkedList<Integer>
    helper = [] #LinkedList<Integer>

    aL = aL + A
    i -= 1
    while i >= 0 and max_component_attachment(aLefts[i], aRights[i]) > minimum:
        if not (aLefts[i] == []) and aLefts[i][-1] > minimum:
            helper = aRights[i]
            aRights[i] = aLefts[i]
            aLefts[i] = helper

        if not (aLefts[i] == []) and aLefts[i][-1] > minimum:
            return False

        aL = aL + aLefts[-1]
        del aLefts[-1]

        aR = aR + aRights[-1]
        del aRights[-1]

        i -= 1

    aLefts.addLast(attachmentSort(aL))
    aRights.addLast(attachmentSort(aR))

    return True


def max_component_attachment(aLefts, aRights):
    resultL = -1;
    resultR = -1;

    if not (aLefts == []):
        resultL = aLefts[-1]

    if not (aRights == []):
        resultR = aRights[-1]

    if resultR > resultL:
        return resultR

    return resultL


def attachmentSort(list_):
    if list_ == []:
        return list_

    size = max(list_)
    to;

    tempList = []

    for i in range(size+1):
        tempList.append(0)

    while not (list_ == []):
        to = list_[0]
        del list_[0]
        tempList.set(to, tempList.get(to) + 1);
    }

    for (int i = 0; i <= size; i++) {
        for (int j = 0; j < tempList.get(i); j++) {
            list_.addLast(i);

    return list_




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


def DFS(graph, lowpoints=True, summary=False):
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

    if summary:
        print("Order: {}" .format(D))
        print("Parents: {}" .format(a))
        print("Articulation points: {}" .format(ap))
        print("Lowpoints L1: {}" .format(low))

    if lowpoints:
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

        if summary:
            print("Lowpoints L1: {}" .format(L1))
            print("Lowpoints L2: {}" .format(L2))
    else:
        L1 = None
        L2 = None

    return D, a, low, ap, L1, L2


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
    for i, comp in enumerate(components):
        graphs.append(Graph(dict((k, graph.get_graph_dict()[k]) for k in list(comp) if k in graph.get_graph_dict())))
        graphs[i].symetrize()

    return graphs


if __name__ == "__main__":
    graph = Graph(g_5)
    print(isPlanar(graph))
