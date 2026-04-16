from network import Network
from graph import GraphImplicit
import numpy as np
class Mission:
    def __init__(self, missions, file):  
        self.missions=missions # list of missions (start, end)
        self._roads = Network.from_file(file)._roads # {node: [(node, length, fatigue),...]}
        self.start, self.end = missions[0][0], missions[-1][1]
        self.FATIGUE_MAX = 1
        for node in self._roads:
            for (v, d, f) in self._roads[node]:
                self.FATIGUE_MAX += f
        

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
    
    def temps_affile(self, missions): 

        # trouver le temps d'affile pour un chemin donné 
        Liste_entiere = [a  for u in missions for a in u]
        list_sommets = []
        for i in range(len(Liste_entiere)-1):
            new_roads = self._roads.copy()
            current_f = self.temps_chemin(list_sommets)[1]
            for a in new_roads:
                new_roads[a] = [(v, d, f+current_f) for (v, d, f) in new_roads[a]]
    
            network = Network(roads=new_roads, start=Liste_entiere[i], end=Liste_entiere[i+1])
            g = network.build_implicit_graph()
            if list_sommets == []:
                list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][1:-1]
            else: list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][2:-1]
        
        return self.temps_chemin(list_sommets), list_sommets
    
    def temps_affile_2(self, precalcul_heuristique=False):
        # construction du graphe
        def fonction_voisin(state):
            if state == self.start:
                return [((self.start, 1, 0), 0)] # on rajoute un 0 pour le nb de missions faites
                    # On commence au point de départ avec une fatigue de 1, coût 0. 

            # Cas d'un état (sommet, fatigue)
            if isinstance(state, tuple):
                u, fatigue_actuelle, nb_missions = state
                voisins = []
                
                for (v, longueur, fatigue_route) in self._roads.get(u, []):
                    nouvelle_fatigue = fatigue_actuelle + fatigue_route
                    temps_parcours = longueur * fatigue_actuelle
                    
                    if u == self.missions[nb_missions]:
                        nb_missions += 1
                    voisins.append(((v, nouvelle_fatigue, nb_missions), temps_parcours))
                
                # Si on est au sommet d'arrivée, on ajoute une transition vers le noeud final
                if u == self.end:
                    voisins.append((self.end, 0))
                    
                return voisins

                # cas du noeud final: il n'a pas de voisins sortants
            return []
        h_dico = {}
        if precalcul_heuristique:
            g_simple_inv = self.build_simple_graph().graphe_inverse()
            h_dico = g_simple_inv.shortest_path(self.end, self.start, return_DISTANCE=True)

        g = GraphImplicit(fonction_voisin, heuristique_dico=h_dico)
        return g.shortest_path2(self.start, self.end, pareto=True, heuristique=True)

    def temps_choix(self): 
        # trouver le temps de choix pour un chemin choisi 
        missions_faites = [(self.start, self.start)]
        liste_sommets = []

        while len(missions_faites) != len(self.missions):
            gr = Network(roads=self._roads, start=missions_faites[-1][1], 
                          end="").build_implicit_graph()
            distance_pt = gr.shortest_path(missions_faites[-1][1], ",kn ", True)
            # Transformer distance_pt pour avoir point = distance
            distance_dict = {k[0]: v for k, v in distance_pt.items()}
            # Sélectionner la mission non faite avec la distance minimale
            remaining_missions = [m for m in self.missions if m not in missions_faites]
            mission = min(remaining_missions, key=lambda x: distance_dict[x[0]])
            missions_faites.append(mission)
            liste_sommets += mission[0]+mission[1]
        return self.temps_affile(missions_faites)

