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
        Ex: edges = {v0: [(v1, 21), (v2, 12)], 
                     v1: [(v0, 74), (v2, 32)], 
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
        for i in range(len(path)-2):
            for a in self._edges[path[i]]:
                if a[0] == path[i+1]: d+= a[1]
        return d

    def shortest_path(self, depart, fin):
        Vu = {}
        DISTANCE = {v:float("inf") for v in self._edges}
        PARENT  = {v:None for v in self._edges}

        DISTANCE[depart] = 0

        node = depart
        while len(Vu) != len(self._edges):
            
            node_distance = DISTANCE[node]
            for voisin, distance in self.neighbours(node):
                voisin_distance = node_distance + distance
                if voisin_distance < DISTANCE[voisin]: 
                    PARENT[voisin] = node
                    DISTANCE[voisin] = voisin_distance
            
            Vu[node] = DISTANCE[node]
            if node == fin: break
            del DISTANCE[node]
            node = Graph.argmin_dico(DISTANCE)
        
        chemin = [fin]
        while chemin[-1] != depart:
            chemin.append(PARENT(chemin[-1]))
        chemin.reverse()
        return (distance(chemin), chemin)

