from network import Network 
import numpy as np
class Mission:
    def __init__(self, missions, file):  
        self.missions=missions # list of missions (start, end)
        self._roads = Network.from_file(file)._roads # {node: [(node, length, fatigue),...]}
        self.temps_affile()

    def temps_chemin(self, path): 
        if path == []: return (0, 0)
        d = 0
        f = 1
        for i in range(0, len(path)-1):
            p1 = path[i][0]
            p2 = path[i+1][0]
            print(p1, p2)
            n0, length, fatigue = list(filter(lambda x: x[0] == p2, self._roads[p1]))[0]
            f += fatigue
            d += length * f
        return (d, f)
    
    def temps_affile(self): 
        # trouver le temps d'affile pour un chemin donné 
        
        Liste_entiere = [a  for u in self.missions for a in u]
        list_sommets = []
        

        for i in range(len(Liste_entiere)-1):
            new_roads = self._roads.copy()
            print("sommets", list_sommets)
            current_f = self.temps_chemin(list_sommets)[1]
            for a in new_roads:
                new_roads[a] = [(v, d, f+current_f) for (v, d, f) in new_roads[a]]
    
            network = Network(roads=new_roads, start=Liste_entiere[i], end=Liste_entiere[i+1])
            g = network.build_implicit_graph()
            if list_sommets == []:
                list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][1:-1]
            else: list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][2:-1]
        print("list des sommets: ", list_sommets)
        print("temps d'affile: ", self.temps_chemin(list_sommets))