from network import Network
from graph import Graph
from time import time
from extension import Mission
# Load the network
network_file = "examples/small.txt"
network = Network.from_file(network_file)
print(network.build_extended_graph().shortest_path("lozere", "saclay"))

def comparaison_duree():
    g = Network.from_file(network_file)
    
    t = time()
    test = g.build_simple_graph().shortest_path(g.start, g.end)
    print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_extended_graph().shortest_path(g.start, g.end)
    print("test extended: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_implicit_graph(pareto=False).shortest_path(g.start, g.end)
    print("test implicite: \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_implicit_graph(pareto=False, heuristique=False).shortest_path(g.start, g.end)[0]
    print("test implicite ++ : \n", "temps: ", time()-t, "\n", "resultat: ", test)

    t = time()
    test = g.build_implicit_graph(pareto=True, heuristique=True).shortest_path(g.start, g.end)[0]
    print("test implicite ++ heuristique: \n", "temps: ", time()-t, "\n", "resultat: ", test)

def test_multitude_missions():
    missions = [("lozere", "guichet"), ("ensae", "saclay")]
    Mission(missions, network_file) 

test_multitude_missions()