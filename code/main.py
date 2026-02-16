from network import Network
from graph import Graph

# Load the network
network_file = "/home/onyxia/work/projet_de_prog/examples/small.txt"
network = Network.from_file(network_file)


g = Network.from_file(network_file)
print(g.build_simple_graph()._edges)
v = g.build_extended_graph() #.shortest_path(g.start, g.end)
print(v.shortest_path(g.start, g.end))

