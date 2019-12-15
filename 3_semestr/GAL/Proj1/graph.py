class Graph(object):
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.graph_dict.keys())

    def get_edges(self):
        return self.__generate_edges()

    def get_graph_dict(self):
        return self.graph_dict

    def get_Adj(self, vertex):
        return self.graph_dict[vertex]

    def add_vertex(self, vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = set()

    def add_edge(self, edge):
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        self.graph_dict[vertex1].add(vertex2)
        self.graph_dict[vertex2].add(vertex1)

    def symetrize(self):
        for i, item in enumerate(self.__generate_edges()):
            if len(item) != 1:
                (vertex1, vertex2) = tuple(item)
                if vertex1 not in self.graph_dict:
                    self.graph_dict[vertex1] = {}
                if vertex2 not in self.graph_dict:
                    self.graph_dict[vertex2] = {}
                if type(self.graph_dict[vertex1]) is dict:
                    self.graph_dict[vertex1] = {vertex2}
                else:
                    self.graph_dict[vertex1].add(vertex2)
                if type(self.graph_dict[vertex2]) is dict:
                    self.graph_dict[vertex2] = {vertex1}
                else:
                    self.graph_dict[vertex2].add(vertex1)

    def remove_self_loops(self):
        vertices = self.get_vertices()
        for i, item in enumerate(vertices):
            if type(self.graph_dict[item]) is not dict:
                self.graph_dict[item] = self.graph_dict[item].difference({item})

    def remove_vertices_of_degree_1(self):
        deleted = set()
        change = True
        while change:
            change = False
            for i, item in enumerate(list(self.graph_dict.keys())):
                if type(self.graph_dict[item]) is not dict:
                    temp = self.graph_dict[item].difference(deleted)
                    if temp != self.graph_dict[item]:
                        self.graph_dict[item] = temp
                        change = True
                if len(self.graph_dict[item]) == 1:
                    deleted = deleted.union(item)
                    del self.graph_dict[item]
                    change = True

    def __generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


class OrderedGraph(object):
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.graph_dict.keys())

    def get_edges(self):
        return self.__generate_edges()

    def get_graph_dict(self):
        return self.graph_dict

    def get_Adj(self, vertex):
        return self.graph_dict[vertex]

    def add_vertex(self, vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


if __name__ == "__main__":
    g = { "a" : {},
          "b" : {"c"},
          "c" : {"b", "c", "d", "e"},
          "d" : {"a", "c"},
          "e" : {"c"},
          "f" : {}
        }

    graph = Graph(g)

    print(graph.graph_dict())

    graph.symetrize()

    print(graph.graph_dict())
