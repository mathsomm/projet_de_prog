from network import Network
from graph import Graph
from time import time
from extension import Mission
import heapq
# Load the network
network_file = "examples/large-smallfatigue.txt"
network = Network.from_file(network_file)
#print(network.build_extended_graph().shortest_path("lozere", "saclay"))

def comparaison_duree():
    g = Network.from_file(network_file)
    
    t = time()
    test = g.build_simple_graph().shortest_path(g.start, g.end)
    print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    '''
    t = time()
    test = g.build_extended_graph().shortest_path2(g.start, g.end)[0]
    print("test extended: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end)[0]
    print("test implicite sans rien: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    '''
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end,pareto=True)[0]
    print("test implicite avec pareto : \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
   
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end,pareto=True, heuristique=True)[0]
    print("test implicite avec pareto et heuristique: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
def test_multitude_missions():
    missions = [("lozere", "guichet"), ("ensae", "saclay")]
    Mission(missions, network_file) 

comparaison_duree()
#test_multitude_missions()