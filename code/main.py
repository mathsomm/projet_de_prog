from network import Network
from graph import Graph
from time import time
# Load the network
network_file = "/home/onyxia/work/projet_de_prog/examples/large-smallfatigue.txt"
network = Network.from_file(network_file)


g = Network.from_file(network_file)

def test_duree(g):
    g = Network.from_file(network_file)

    t = time()
    #test = g.build_simple_graph().shortest_path(g.start, g.end)
    #print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    #test = g.build_extended_graph().shortest_path(g.start, g.end)
    #print("test extended: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    #test = g.build_implicit_graph(pareto=False).shortest_path(g.start, g.end)
    #print("test implicite: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_implicit_graph(pareto=True, heuristique=False).shortest_path(g.start, g.end)
    print("test implicite ++ : \n", "temps: ", time()-t, "\n", "resultat: ", test)


    t = time()
    test = g.build_implicit_graph(pareto=True, heuristique=True).shortest_path(g.start, g.end)
    print("test implicite ++ : \n", "temps: ", time()-t, "\n", "resultat: ", test)
test_duree(g)