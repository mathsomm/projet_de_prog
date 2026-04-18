from network import Network
from graph import Graph
from time import time
from extension import Mission, Time_comparer
import heapq


# Load the network
network_file = "examples/medium-smallfatigue.txt"
network = Network.from_file(network_file)


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
    missions = [("v0", "v5"), ("v5", "v10"), ("v15", "v40"), ("v7", "v30")]
    m = Mission(missions, network_file)
    #print(m.temps_choix(), "\n--------")
    print(m.temps_affile_2(True))



#comparaison_duree()
#test_multitude_missions()
t = Time_comparer(max_nodes=1000000, step= 9 , repetitions = 50, loi_log=True)
#t = Time_comparer(max_nodes=1000000, step= 100000, repetition = 100)

mission_test = Mission( [("v0", "v1"), ("v4", "v0"), ("v3", "v4")], "",
        {
            "v0": [("v1", 100, 2), ("v2", 10, 15)],
            "v1": [("v2", 200, 4)],
            "v2": [("v3", 100, 4)],
            "v3": [("v4", 80, 5), ("v5", 100, 1)],
            "v4": [("v5", 10, 1)],
            "v5": [("v0", 75, 1)],

        }
    )
print(mission_test.temps_affile())
print()
print(mission_test.temps_choix())