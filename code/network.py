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

        self.FATIGUE_MAX = 0
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
        edge_fatigue=self._roads
        for e in self._roads:
            edges[e]=[]
            for c in self._roads[e]:
                edges[e].append((c[0],c[1]))
        simple_graph=Graph(edges)
        return simple_graph
    
    def build_extended_graph(self) -> Graph:
        New_roads = {}
        print("FATIGUE MAX: ", self.FATIGUE_MAX)
        for node in self._roads:
            for i in range(self.FATIGUE_MAX):
                New_roads[(node, i)] = []
                for (v, d, f) in self._roads[node]:
                    New_roads[(node, i)].append(((v, i+f), d+f))

        # rajout du node début et fin
        New_roads[self.start] = [((self.start, i), 0) for i in range(self.FATIGUE_MAX)]
        for i in range(self.FATIGUE_MAX):
            if (self.end, i) not in New_roads: New_roads[(self.end, i)] = []
            New_roads[(self.end, i)].append((self.end,0))
        New_roads[self.end] = []

        return Graph(New_roads)
