from network import Network
from graph import Graph

# Load the network
network_file = "/home/onyxia/projet_de_prog/examples/small.txt"
network = Network.from_file(network_file)


g = Network.from_file(network_file)
g.print_result()
