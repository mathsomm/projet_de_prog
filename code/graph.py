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
            if node == fin:
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
 
class GraphImplicit(Graph):
        def __init__(self, fonction_voisins, heuristique_info={}):
            self.fonction_voisins = fonction_voisins
            self.heuristique_info = heuristique_info
        
        def neighbours(self, node):
            return self.fonction_voisins(node) 

        def heuristique(self, a, dico):
            if type(a)==tuple and self.heuristique_info != {} and a[0] in self.heuristique_info:
                distance_fin = self.heuristique_info[a[0]]
                fatigue = a[1]
                if dico[a] == 0: return 0
                return distance_fin*fatigue + dico[a]
            return dico[a]

edges={'v0': [('v1', 21), ('v2', 12)], 'v1': [('v0', 74), ('v2', 32)]}