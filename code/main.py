from network import Network
from graph import Graph

# Load the network
network_file = "/home/onyxia/work/projet_de_prog/examples/small.txt"
network = Network.from_file(network_file)

print("test commit push")
print("test pull")

g = Network.from_file(network_file).build_simple_graph()
v = g.shortest_path("lozere", "saclay")
print(g._edges)
print(v)