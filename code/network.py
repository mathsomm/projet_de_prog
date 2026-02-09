from graph import *

class Network:
    """
    Class for a network that represents the environment (with length and fatigue on roads). 
    """

    def __init__(self, roads={}, start=None, end=None):
        """
        Initializes the network from a dictionary roads. 

        Parameters: 
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list, that is 
            roads[u] = list of (v, length, fatigue)
            Ex: roads = {v0: [(v1, 21, 2), (v2, 12, 4)], 
                        v1: [(v0, 74, 2), (v2, 32, 1)], 
                        ...}
        start, end: 
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

    def __str__(self): 
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Network from an environment file.

        File format: one edge per line (start end length fatigue).
        """
        # Initialize adjacency list
        roads = {}

        with open(filename, "r") as testcase:
            nb, start, end = testcase.readline().strip().split()
            for _ in range(int(nb)):
                i, j, l, f = testcase.readline().strip().split()
                l, f = int(l), int(f)
                roads.setdefault(i, []).append((j, l, f))
                roads.setdefault(j, [])

        return cls(roads=roads, start=start, end=end)
    
   

    def build_simple_graph(self) -> Graph:
        """
        Builds an object of type Graph from the network, by ignoring the fatigue coefficient. 
        """
        edges={}
        edge_fatigue=self._roads
        for e in self._roads:
            edges[e]=[]
            for c in self._roads[e]:
                edges[e].append((c[0],c[1]))
        simple_graph=Graph(edges)
        return simple_graph
    
    def build_extended_graph(self) -> Graph:
        # Parcours en largeur
        VUS = []
        file = [self.start]
        new_graph = {self.start: []}
        graph_antecedent = self.build_simple_graph().graphe_inverse()
        stockage = {}

        while file != []:
            sommet = file [0]
            VUS.append(sommet)

            # rajouter les voisins aux sommets à étudier 
            for v in self._roads[sommet]:
                if v not in VUS and v not in file: 
                    file.append(v)

            # Créer le graphe 
            # regarde les antécédents 
            for v in graph_antecedent[sommet]:
                # distance au nouveau graphe c'est la distance précédente + la somme des fatigues
                
                nouvelle_fatigue = new_graph[v][0][2] + graph[v][sommet][2] # on prend l'élément 0 car tt les sommets ont un unique précédent
                nouvelle_distance = nouvelle_fatigue + graph[v][sommet][1]    
                new_graph[v] = [((v + "-" + sommet, nouvelle_distance, nouvelle_fatigue))]
            
            del file[0]

            
                
            


        
network=Network({'v0': [('v1', 21, 2), ('v2', 12, 4)], 
                        'v1': [('v0', 74, 2), ('v2', 32, 1)]})

graph=network.build_simple_graph()
print(graph._edges)

