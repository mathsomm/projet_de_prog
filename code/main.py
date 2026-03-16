from network import Network
from graph import Graph
from time import time
# Load the network
network_file = "/home/onyxia/work/projet_de_prog/examples/medium-largefatigue.txt"
network = Network.from_file(network_file)


g = Network.from_file(network_file)
g.print_result()


def test_duree(g):
    g = Network.from_file(network_file)

    t = time()
    test = g.build_simple_graph().shortest_path(g.start, g.end)
    print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_extanded_graph().shortest_path(g.start, g.end)
    print("test extanded: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_build_implicit_graph(pareto=False).shortest_path(g.start, g.end)
    print("test implicite: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_build_implicit_graph(pareto=True).shortest_path(g.start, g.end)
    print("test implicite ++ : \n", "temps: ", time()-t, "\n", "resultat: ", test)

test_duree(g)