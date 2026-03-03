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
            Ex: roads = {'v0': [('v1', 21, 2), ('v2', 12, 4)], 
                        'v1': [('v0', 74, 2), ('v2', 32, 1)]}
        start, end: 
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

        self.FATIGUE_MAX = 1
        for node in self._roads:
            for (v, d, f) in self._roads[node]:
                self.FATIGUE_MAX += f

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
        for e in self._roads:
            edges[e]=[]
            for c in self._roads[e]:
                edges[e].append((c[0],c[1]))
        simple_graph=Graph(edges)
        return simple_graph
    
    def print_result(self):
        R = self.build_extended_graph().shortest_path(self.start, self.end)
        print("--RESULTAT--")
        print("TEMPS MINIMAL:", R[0])
        print("TRAJET", R[1])

        print("\n \n--INFO--")
        print("MAX fatigue: ", self.FATIGUE_MAX)
        print("NB Node: ", len(self._roads))
        print("Roads", list(self._roads.keys()))

    def build_extended_graph(self) -> Graph:
        New_roads = {}
        for node in self._roads:
            for i in range(1, self.FATIGUE_MAX+1):
                New_roads[(node, i)] = []
                for (v, d, f) in self._roads[node]:
                    New_roads[(node, i)].append(((v, i+f), d*i))

        # rajout du node début et fin
        New_roads[self.start] = [((self.start, 1), 0)]
        for i in range(1, self.FATIGUE_MAX+1):
            if (self.end, i) not in New_roads: New_roads[(self.end, i)] = []
            New_roads[(self.end, i)].append((self.end,0))
        New_roads[self.end] = []
        return Graph(New_roads)


#Explication du fonctionnement de la méthode build_implicit_graph: elle fabrique un objet GraphImplicit et lui donne la fonction  "fonction_voisins" qui va avec
    
    def build_implicit_graph(self) -> GraphImplicit:
        def fonction_voisins(state):  #on définit ici la fameuse focntion qui permet de récupérer les voisins. C'est celle qui est utilisée par GraphImplicit
            if state == self.start:
                return [((self.start, 1), 0)]
                # On commence au point de départ avec une fatigue de 1, coût 0. En effet, il faut faire le pond entre le départ dans le monde simple et le départ dans le monde étnedu

            # Cas d'un état (sommet, fatigue)
            if isinstance(state, tuple):
                u, fatigue_actuelle = state
                voisins = []
                
                for (v, longueur, fatigue_route) in self._roads.get(u, []):
                    nouvelle_fatigue = fatigue_actuelle + fatigue_route
                    temps_parcours = longueur * fatigue_actuelle
                    voisins.append(((v, nouvelle_fatigue), temps_parcours))
                
                # Si on est au sommet d'arrivée, on ajoute une transition vers le noeud final
                if u == self.end:
                    voisins.append((self.end, 0))
                    
                return voisins

            # cas du noeud final: il n'a pas de voisins sortants
            return []

        # On retourne un objet GraphImplicit qui utilisera cette fonction
        return GraphImplicit(fonction_voisins)

#network_test = Network({'v0': [('v1', 21, 2), ('v2', 12, 4)], 
                        'v1': [('v0', 74, 2), ('v2', 32, 1)],'v2':[('v3',15,2)]},'v0','v3')
#print(network_test._roads)
#print(network_test.build_implicit_graph().neighbours(('v0',2)))
#print(network_test.build_implicit_graph().shortest_path('v0','v3'))
