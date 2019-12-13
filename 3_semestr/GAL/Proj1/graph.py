""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""

class Graph(object):
    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = set()

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        self.__graph_dict[vertex1].add(vertex2)

    def symetrize(self):
        for i, item in enumerate(self.__generate_edges()):
            if len(item) != 1:
                (vertex1, vertex2) = tuple(item)
                if type(self.__graph_dict[vertex1]) is dict:
                    self.__graph_dict[vertex1] = {vertex2}
                else:
                    self.__graph_dict[vertex1].add(vertex2)
                if type(self.__graph_dict[vertex2]) is dict:
                    self.__graph_dict[vertex2] = {vertex1}
                else:
                    self.__graph_dict[vertex2].add(vertex1)

    def remove_self_loops(self):
        vertices = self.vertices()
        for i, item in enumerate(vertices):
            if type(self.__graph_dict[item]) is not dict:
                self.__graph_dict[item] = self.__graph_dict[item].difference({item})

    def remove_vertexes_of_degree_1(self):
        deleted = set()
        change = True
        while change:
            change = False
            for i, item in enumerate(list(self.__graph_dict.keys())):
                if type(self.__graph_dict[item]) is not dict:
                    temp = self.__graph_dict[item].difference(deleted)
                    if temp != self.__graph_dict[item]:
                        self.__graph_dict[item] = temp
                        change = True
                if len(self.__graph_dict[item]) == 1:
                    deleted = deleted.union(item)
                    del self.__graph_dict[item]
                    change = True

    def graph_dict(self):
        return self.__graph_dict

    def get_Adj(self, vertex):
        return self.__graph_dict[vertex]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
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
    #print("Vertices of graph:")
    #print(graph.vertices())

    #print("Edges of graph:")
    print(graph.graph_dict())

    #print("Add vertex:")
    #graph.add_vertex("z")

    #print("Vertices of graph:")
    #print(graph.vertices())
 
    #print("Add an edge:")
    #graph.add_edge({"a","z"})
    #graph.add_edge({"a","z"})
    #graph.add_edge({"a","z"})
    #
    #print("Vertices of graph:")
    #print(graph.vertices())

    #print("Edges of graph:")
    #print(graph.edges())

    #print('Adding an edge {"x","y"} with new vertices:')
    #graph.add_edge({"x","y"})
    #print("Vertices of graph:")
    #print(graph.vertices())
    #print("Edges of graph:")
    #print(graph.edges())
