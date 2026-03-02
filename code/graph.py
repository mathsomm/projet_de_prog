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

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def argmin_dico(dico):
        m = float("inf")
        mini = None
        for i in dico:
            if dico[i] < m:
                mini = i
                m = dico[i]
        return mini

    def distance(self, path):
        d = 0
        for i in range(len(path)-1):
            for a in self._edges[path[i]]:
                if a[0] == path[i+1]: d += a[1]
        return d

    def shortest_path(self, depart, fin) -> tuple:
    
        DISTANCE = {depart: 0} # DISTANCE ne contient que les nœuds "découverts"
        PARENT = {depart: None}
        Vu = {} #Un sommet est dans Vu quand on sait avec certitude avoir trouvé son chemin et sa distance optimale
        while DISTANCE:
            node = Graph.argmin_dico(DISTANCE)# On cherche le nœud le plus proche parmi ceux qu'on connaît
            if node is None:
                break
            node_distance = DISTANCE[node]
            # Si on a atteint la destination, on peut s'arrêter
            if node == fin:
                Vu[node] = node_distance
                break
            #exploration des voisins   
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
        # Reconstruction du chemin
        if fin not in Vu:
            return (float("inf"), [])
        chemin = []
        actuel = fin
        while actuel is not None:
            chemin.append(actuel)
            actuel = PARENT[actuel]
        chemin.reverse()
        return (Vu[fin], chemin)


    class GraphImplicit(Graph):
        def __init__(self, fonction_voisins):
            self.fonction_voisins = fonction_voisins
        
        def neighbours(self, node):
            return self.fonction_voisins(node)  



    







edges_test = {'v0': [('v1', 21), ('v2', 12)], 'v1': [('v0', 10), ('v2', 0),('v3',4)],'v2':[('v3',70)]}
graph_test = Graph(edges_test)
print(graph_test.shortest_path('v0','v3'))