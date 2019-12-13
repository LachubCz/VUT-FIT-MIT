import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):

    G=nx.Graph()

    G.add_nodes_from(graph.vertices())
    G.add_edges_from(graph.edges())

    nx.draw(G)
    plt.show()
