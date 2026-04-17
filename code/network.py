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
        self.mémoire_pareto={} #{v:[(fatigue1,distance1),(fatigue2,distance2),...]}

    def __str__(self): 
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def create_graph(cls, nb_nodes, distance_range=(10, 1000), fatigue_range=(1, 10), start=None, end=None):
        import random
        from collections import deque
        
        # Generate node names
        nodes = [f"v{i}" for i in range(nb_nodes)]
        
        # Choose start and end nodes if not specified
        if start is None:
            start = random.choice(nodes)
        if end is None:
            end = random.choice(nodes)
            # Make sure start and end are different
            while end == start:
                end = random.choice(nodes)
        
        # Generate random number of edges
        nb_edges = random.randint(nb_nodes, nb_nodes * 20)
        
        # Initialize adjacency list with all nodes
        roads = {node: [] for node in nodes}
        
        # Create a guaranteed path from start to end
        # by selecting random intermediate nodes and connecting them in sequence
        path_nodes = [start]
        remaining_nodes = [n for n in nodes if n != start and n != end]
        random.shuffle(remaining_nodes)
        
        # Add 1-3 random intermediate nodes to the path
        num_intermediate = random.randint(1, len(remaining_nodes)//10 +1)
        print("num_intermediate", num_intermediate, "remaining_nodes", len(remaining_nodes))
        path_nodes.extend(remaining_nodes[:num_intermediate])
        path_nodes.append(end)
        
        # Create edges along the guaranteed path
        edges_created = 0
        for i in range(len(path_nodes) - 1):
            u, v = path_nodes[i], path_nodes[i + 1]
            distance = random.randint(distance_range[0], distance_range[1])
            fatigue = random.randint(fatigue_range[0], fatigue_range[1])
            roads[u].append((v, distance, fatigue))
            edges_created += 1
        
        # Create additional random edges until we reach the target number
        max_attempts = nb_edges * 5  # Avoid infinite loop
        attempts = 0
        
        while edges_created < nb_edges and attempts < max_attempts:
            attempts += 1
            
            # Pick two random different nodes
            u = random.choice(nodes)
            v = random.choice(nodes)
            
            if u == v:
                continue
            
            # Check if edge already exists
            if any(dest == v for dest, _, _ in roads[u]):
                continue
            
            # Generate random distance and fatigue
            distance = random.randint(distance_range[0], distance_range[1])
            fatigue = random.randint(fatigue_range[0], fatigue_range[1])
            
            # Add edge (directed)
            roads[u].append((v, distance, fatigue))
            edges_created += 1
        
        print(f"Generated graph with {nb_nodes} nodes and {edges_created} edges")
        print(f"Start: {start}, End: {end}")
        print(f"✅ Guaranteed path exists: {len(path_nodes)}")
        
        return cls(roads=roads, start=start, end=end)

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
        # afficher les resultats associés au plus court chemin
        R = self.build_implicit_graph().shortest_path(self.start, self.end)
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


    # fabrique un objet GraphImplicit et lui donne la fonction "fonction_voisins" qui va avec
    def build_implicit_graph(self, précalcul_heuristique=True) -> GraphImplicit:
        
        def fonction_voisins(state):  # on définit ici la focntion qui permet de récupérer les voisins. C'est celle qui est utilisée par GraphImplicit
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
        
        h_dico = {}
        if précalcul_heuristique:
            g_simple_inv = self.build_simple_graph().graphe_inverse()
            h_dico = g_simple_inv.shortest_path(self.end, self.start, return_DISTANCE=True)
    
        return GraphImplicit(fonction_voisins, heuristique_dico=h_dico)
    