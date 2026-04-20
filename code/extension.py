from network import Network
from graph import GraphImplicit
import numpy as np
class Mission:
    def __init__(self, missions, file, _roads = {}):  
        self.missions=missions # list of missions (start, end)
        if _roads == {}:
            self._roads = Network.from_file(file)._roads # {node: [(node, length, fatigue),...]}
        else: self._roads = _roads
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
            n0, length, fatigue = list(filter(lambda x: x[0] == p2, self._roads[p1]))[0]
            f += fatigue
            d += length * f
        return (d, f)
    
    def temps_affile(self): 

        # trouver le temps d'affile pour un chemin donné 
        Liste_entiere = [a  for u in self.missions for a in u]
        list_sommets = []
        for i in range(len(Liste_entiere)-1):

            network = Network(roads=self._roads, start=Liste_entiere[i], end=Liste_entiere[i+1])
            g = network.build_extended_graph()
            if list_sommets == []:
                list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][1:-1]
            else: list_sommets += g.shortest_path(Liste_entiere[i], Liste_entiere[i+1])[1][2:-1]
        return self.temps_chemin(list_sommets), list_sommets
    
    def temps_affile_2(self, precalcul_heuristique=False):
        # construction du graphe
        def fonction_voisin(state):
            L = [a  for u in self.missions for a in u]
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
                    
                    if nb_missions < len(L) and u == L[nb_missions]:
                        nb_missions += 1
                    voisins.append(((v, nouvelle_fatigue, nb_missions), temps_parcours))
                
                # Si on est au sommet d'arrivée, on ajoute une transition vers le noeud final
                if u == self.end and nb_missions==len(L):
                    voisins.append((self.end, 0))
                return voisins

                # cas du noeud final: il n'a pas de voisins sortants
            return []
        h_dico = {}
        if precalcul_heuristique:
            g_simple_inv = self.build_simple_graph().graphe_inverse()
            h_dico = g_simple_inv.shortest_path(self.end, self.start, return_DISTANCE=True)

        g = GraphImplicit(fonction_voisin, heuristique_dico=h_dico)
        return g.shortest_path(self.start, self.end)

    def temps_choix(self): 
        # trouver le temps de choix pour un chemin choisi 
        missions_faites = [(self.start, self.start)]
        liste_sommets = []
        while len(missions_faites) != len(self.missions):
            gr = Network(roads=self._roads, start=missions_faites[-1][1], 
                          end="")
            distance_pt = gr.build_extended_graph().shortest_path(missions_faites[-1][1], "v4", True)
            print(missions_faites[-1][1])
            # Transformer distance_pt pour avoir point = distance
            distance_dict = {k[0]: v for k, v in distance_pt.items()}
            # Sélectionner la mission non faite avec la distance minimale
            remaining_missions = [m for m in self.missions if m not in missions_faites]
            mission = min(remaining_missions, key=lambda x: distance_dict[x[0]])
            print("je fais la mission", mission)
            missions_faites.append(mission)
            liste_sommets += mission[0]+mission[1]
        self.missions, save = missions_faites, self.missions
        v = self.temps_affile()
        self.missions = save
        return v

class Time_comparer:
    def __init__(self,  max_nodes=50, step=5, repetitions=3, loi_log=False):
        sizes, results = self.compare_different_size(max_nodes, step, repetitions, loi_log)
        self.plot_results(sizes, results)

    def compare_different_size(self, max_nodes=50, step=5, repetitions=3, loi_log=False):
        sizes = list(range(10, max_nodes + 1, step))
        from math import log10
        from time import time
        if loi_log: 
            B = [k*10**i for i in range(2, int(log10(max_nodes)))  for k in range(1, 10)]
            sizes = [B[step*k] for k in range(0, len(B)//step)]
        results = {
            "simple_graph": [],
            "implicit_graph_no_heuristic": [],
            "implicit_graph_with_heuristic": [],
            "implicit_pareto": [],
            "implicit_pareto_heuristic": []
        }
        
        print("Début du test")
        print("Tailles testées:", sizes)
        print("Répétitions par taille:", repetitions)
        
        for size in sizes:
            print("Test avec", size, " noeuds")
            
            times_simple = []
            times_implicit_no_h = []
            times_implicit_h = []
            times_pareto = []
            times_pareto_h = []
            
            for rep in range(repetitions):
                # Créer un graphe aléatoire
                # graphe fatigue
                g = Network.create_graph(size, distance_range=(10, 100), fatigue_range=(1, 1000))
                
                # Test 1: Simple graph
                
                t = time()
                g.build_simple_graph().shortest_path(g.start, g.end)
                times_simple.append(time() - t)

                
                # Test 2: Implicit graph without heuristic, no pareto
                t = time()
                g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end, pareto=False)
                times_implicit_no_h.append(time() - t)

                
                # Test 3: Implicit graph with heuristic, no pareto
                t = time()
                g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end, pareto=False, heuristique=True)
                times_implicit_h.append(time() - t)

                
                # Test 4: Implicit graph with pareto, no heuristic
                t = time()
                g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end, pareto=True)
                times_pareto.append(time() - t)
                
                # Test 5: Implicit graph with pareto and heuristic
                t = time()
                g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end, pareto=True, heuristique=True)
                times_pareto_h.append(time() - t)

            
            # Calculer la moyenne des temps
            if times_simple:
                results["simple_graph"].append(np.mean(times_simple))
            else:
                results["simple_graph"].append(0)
                
            if times_implicit_no_h:
                results["implicit_graph_no_heuristic"].append(np.mean(times_implicit_no_h))
            else:
                results["implicit_graph_no_heuristic"].append(0)
                
            if times_implicit_h:
                results["implicit_graph_with_heuristic"].append(np.mean(times_implicit_h))
            else:
                results["implicit_graph_with_heuristic"].append(0)
                
            if times_pareto:
                results["implicit_pareto"].append(np.mean(times_pareto))
            else:
                results["implicit_pareto"].append(0)
                
            if times_pareto_h:
                results["implicit_pareto_heuristic"].append(np.mean(times_pareto_h))
            else:
                results["implicit_pareto_heuristic"].append(0)
            print("Resultat temps pareto", results["implicit_pareto"][-1])
        
        return sizes, results

    def plot_results(self, sizes, results):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 7))
        
        plt.plot(sizes, results["simple_graph"], marker='o', label="Simple Graph", linewidth=2)
        plt.plot(sizes, results["implicit_graph_no_heuristic"], marker='s', label="Implicit (No Heuristic)", linewidth=2)
        plt.plot(sizes, results["implicit_graph_with_heuristic"], marker='^', label="Implicit (With Heuristic)", linewidth=2)
        plt.plot(sizes, results["implicit_pareto"], marker='d', label="Implicit (Pareto)", linewidth=2)
        plt.plot(sizes, results["implicit_pareto_heuristic"], marker='*', label="Implicit (Pareto + Heuristic)", linewidth=2, markersize=10)
        
        plt.xlabel('Nombre de nœuds', fontsize=12)
        plt.ylabel('Temps (secondes)', fontsize=12)
        plt.title('Temps de calcul du plus court chemin\nselon la taille du graphe', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plt.savefig('results.png', dpi=300)
        print("\n !!!!! Graphique sauvegardé: !!!! results.png")
        plt.show()
