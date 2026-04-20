from network import Network
from graph import Graph
from time import time
from extension import Mission, Time_comparer
import heapq


# Load the network



def comparaison_duree():
    g = Network.from_file(network_file)
    
    t = time()
    test = g.build_simple_graph().shortest_path(g.start, g.end)
    print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
    t = time()
    test = g.build_extended_graph().shortest_path2(g.start, g.end)[0]
    print("test extended: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end)[0]
    print("test implicite sans rien: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end,pareto=True)[0]
    print("test implicite avec pareto : \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
   
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end,pareto=True, heuristique=True)[0]
    print("test implicite avec pareto et heuristique: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
def test_multitude_missions():
    mission_test = Mission( [("v0", "v2"), ("v4", "v0"), ("v3", "v4")], "",
        {
            "v0": [("v1", 100, 2), ("v2", 10, 15)],
            "v1": [("v2", 200, 4)],
            "v2": [("v3", 100, 4)],
            "v3": [("v4", 80, 5), ("v5", 100, 1)],
            "v4": [("v5", 10, 1)],
            "v5": [("v0", 75, 1)],

        }
    )
    print("Le temps minimal possible est:", mission_test.temps_affile_2())

#####################################################################
#################         CODE      #####################################
#####################################################################
network_file = "examples/medium-smallfatigue.txt"
network = Network.from_file(network_file)

# Pour tester le bon fonctionnement de l'algorithme
r = network.build_implicit_graph().shortest_path2(network.start, network.end, pareto=True, heuristique=False)
#print(r)

# Pour tester le temps des différents algorithmes sur ce fichier
#comparaison_duree()

# Pour tester le temps des différents algorithmes sur un ensemble de graphes créés aléatoirement + sauvegarde photo
#t = Time_comparer(max_nodes=1000, step= 100, repetitions = 10)
#t = Time_comparer(max_nodes=10000, step= 3 , repetitions = 5, loi_log=True)


# Pour tester l'algorithme avec missions:
test_multitude_missions()





