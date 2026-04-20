import heapq

"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""


class Graph:
    """
    A minimal class for directed weighted graph represented as adjacency list. 
    
    Attributes: 
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight.
        Ex: edges = {'v0': [('v1', 21), ('v2', 12)], 
                     'v1': [('v0', 74), ('v2', 32)], 
                     ...}

    Methods: 
    --------
    neighbours(self, node): 
        Returns the list of all neighbors of a node
    """

    def __init__(self, edges):
        self._edges = edges

    def heuristique(self, a, dico): return dico[a]
    
    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def argmin_dico(self, dico):
        m = float("inf")
        mini = None
        for i in dico:
            if self.heuristique(i, dico) < m:
                mini = i
                m = self.heuristique(i, dico)
        if mini == None: print("argmin_dico: mini is None")
        return mini

    def graphe_inverse(self):
        roads_inv={}
        for v in self._edges:
            for (e,d) in self._edges[v]:
                if e not in roads_inv: roads_inv[e]=[(v,d)]
                else: roads_inv[e].append((v,d))
        return Graph(roads_inv)


    def distance(self, path): 
        # trouver la distance parcourue pour un chemin donné 
        d = 0
        for i in range(len(path)-1):
            for a in self._edges[path[i]]:
                if a[0] == path[i+1]: d += a[1]
        return d

    def shortest_path(self, depart, fin, return_DISTANCE = False) -> tuple:
        
        DISTANCE = {depart: 0} # DISTANCE ne contient que les nœuds "découverts"
        PARENT = {depart: None}
        Vu = {} #Un sommet est dans Vu quand on sait avec certitude avoir trouvé son chemin et sa distance optimale
        while DISTANCE != {}:
            node = self.argmin_dico(DISTANCE)# On cherche le nœud le plus proche parmi ceux qu'on connaît
            if node is None:
                print("plus de node, on arrête")
                break
            node_distance = DISTANCE[node]
            # Si on a atteint la destination, on peut s'arrêter
            if node == fin and not return_DISTANCE:
                Vu[node] = node_distance
                break
            #exploration des voisins   
            #print("voisins:", list(self.neighbours(node)))
            for (voisin, poids_arete) in self.neighbours(node):
                if voisin in Vu:
                    continue
                nouvelle_dist = node_distance + poids_arete
                
                # Si le voisin est inconnu OU si on a trouvé un chemin plus court
                if voisin not in DISTANCE or nouvelle_dist < DISTANCE[voisin]:
                    DISTANCE[voisin] = nouvelle_dist
                    PARENT[voisin] = node
            # On marque le nœud comme visité et on le retire des candidats
            Vu[node] = DISTANCE.pop(node)
        if return_DISTANCE: return Vu
        
        # Reconstruction du chemin
        if fin not in Vu:
            print("ou est la fin")
            return (float("inf"), [])
        chemin = []
        actuel = fin
        while actuel is not None:
            chemin.append(actuel)
            actuel = PARENT[actuel]
        chemin.reverse()
        return (Vu[fin], chemin)

    def shortest_path2(self, depart, fin, pareto=False, heuristique=False):
        # Format : (f_score, temps_total_cumulé, fatigue_actuelle, noeud_actuel, noeud_parent)
        atraiter = []
        heapq.heappush(atraiter, (0, 0, 1, depart, None))
        archives_pareto = {}
        PARENT = {}
        while atraiter: # Tant qu'il y a des noeuds à explorer
            # on incorpore ici en plus la méthode de prunning
            f_score, temps_total, fatigue, u, parent = heapq.heappop(atraiter)
            if pareto: 
                if u in archives_pareto: 
                    estdominé=False
                    for (f_archive, t_archive) in archives_pareto[u]:
                        if f_archive <= fatigue and t_archive <= temps_total:
                            estdominé=True
                            break
                    if estdominé: 
                        continue 
                    else: 
                        archives_pareto[u].append((fatigue,temps_total))
                        PARENT[(u, fatigue)] = parent
                else:
                    archives_pareto[u]=[(fatigue,temps_total)]
                    PARENT[(u, fatigue)] = parent
            else: 
                if (u, fatigue) in PARENT:
                    continue
                PARENT[(u, fatigue)] = parent
            
            # condition d'arret
            if u == fin:
                chemin = []
                var = (u, fatigue) 
                while var is not None:
                    chemin.append(var[0]) 
                    var = PARENT[var]
                chemin.reverse()
                return (temps_total, chemin)
            # Ajout des voisins dans atraiter
            for state_voisin, poids_arete in self.neighbours((u, fatigue)):
                v, nouvelle_fatigue = state_voisin
                nouveau_temps_total = temps_total + poids_arete 
                # Calcul du A* : f(n) = g(n) + h(n)
                # (Il faudra
                if heuristique:
                    h_score = self.heuristique(v, nouvelle_fatigue)
                    nouveau_f_score = nouveau_temps_total + h_score
                else:
                    nouveau_f_score = nouveau_temps_total
                # On ajoute à la file de priorité
                heapq.heappush(atraiter, (nouveau_f_score, nouveau_temps_total, nouvelle_fatigue, v, (u, fatigue)))

        # Si on sort du while sans avoir trouvé 'fin', c'est qu'il n'y a pas de chemin
        return (float("inf"), [])




class GraphImplicit(Graph):
    
    def __init__(self, fonction_voisins, heuristique_dico=None):
        self.fonction_voisins = fonction_voisins
        if heuristique_dico:
            self.heuristique_dico = heuristique_dico
        else:
            self.heuristique_dico = {}
   
    def neighbours(self, node):
        return self.fonction_voisins(node)

    def heuristique(self, v, fatigue):
        if v in self.heuristique_dico:
            return self.heuristique_dico[v] * fatigue
        return 0
    
    


            

