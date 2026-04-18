import sys 
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

#import pytest
from network import Network
from extension import Mission

def test_network_small():
    # Setup
    network = Network.from_file(NET_DIR / "small.txt")
    
    # Assertions
    assert network.start == "lozere"
    assert network.end == "saclay"
    assert network._roads == {
        'lozere': [('ensae', 10, 2), ('guichet', 20, 0)], 
        'ensae': [('saclay', 45, 0)], 
        'guichet': [('ensae', 15, 1)],
        'saclay': []
    }

def test_build_simple_graph():
    network = Network.from_file(NET_DIR / "small.txt")

    simple_graph = network.build_simple_graph()
    assert simple_graph._edges == {
        'lozere': [('ensae', 10), ('guichet', 20)], 
        'ensae': [('saclay', 45)], 
        'guichet': [('ensae', 15)],
        'saclay': []
    }


def test_build_extended_graph():
    network = Network.from_file(NET_DIR / "small.txt")

    extended_graph = network.build_extended_graph()
    assert extended_graph._edges == {
        ('lozere', 1): [(('ensae', 3), 10), (('guichet', 1), 20)], 
        ('lozere', 2): [(('ensae', 4), 20), (('guichet', 2), 40)], 
        ('lozere', 3): [(('ensae', 5), 30), (('guichet', 3), 60)], 
        ('lozere', 4): [(('ensae', 6), 40), (('guichet', 4), 80)], 
        ('ensae', 1): [(('saclay', 1), 45)], 
        ('ensae', 2): [(('saclay', 2), 90)], 
        ('ensae', 3): [(('saclay', 3), 135)], 
        ('ensae', 4): [(('saclay', 4), 180)], 
        ('guichet', 1): [(('ensae', 2), 15)], 
        ('guichet', 2): [(('ensae', 3), 30)], 
        ('guichet', 3): [(('ensae', 4), 45)], 
        ('guichet', 4): [(('ensae', 5), 60)], 
        ('saclay', 1): [('saclay', 0)], 
        ('saclay', 2): [('saclay', 0)], 
        ('saclay', 3): [('saclay', 0)], 
        ('saclay', 4): [('saclay', 0)], 
        'lozere': [(('lozere', 1), 0)], 
        'saclay': []}

def test_shortest_path():
    network = Network.from_file(NET_DIR / "small.txt")
    extended_graph = network.build_extended_graph()
    result = extended_graph.shortest_path(network.start, network.end)
    assert result[0] == 125
    assert result[1] == ['lozere', ('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), 'saclay']


def test_shortest_path_2():
    network = Network.from_file(NET_DIR / "small.txt")
    extended_graph = network.build_implicit_graph(précalcul_heuristique=True)
    
    result = extended_graph.shortest_path2(network.start, network.end, pareto=True, heuristique=True) 
    assert result[0] == 125
    assert result[1] == ['lozere', ('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), 'saclay']

    result = extended_graph.shortest_path2(network.start, network.end, pareto=False, heuristique=True) 
    assert result[0] == 125
    assert result[1] == ['lozere', ('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), 'saclay']

    result = extended_graph.shortest_path2(network.start, network.end, pareto=True, heuristique=False) 
    assert result[0] == 125
    assert result[1] == ['lozere', ('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), 'saclay']

    result = extended_graph.shortest_path2(network.start, network.end, pareto=False, heuristique=False) 
    assert result[0] == 125
    assert result[1] == ['lozere', ('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), 'saclay']

def test_neighbours_GraphImplicit():
    network_test = Network({'v0': [('v1', 21, 2), ('v2', 12, 4)], 'v1': [('v0', 74, 2), ('v2', 32, 1)],'v2':[('v3',15,2)]},'v0','v3')
    
    n = network_test.build_implicit_graph().neighbours(('v0',2))
    assert n == [(('v1', 4), 42), (('v2', 6), 24)]


def test_missions():
    mission_test = Mission( [("v0", "v1"), ("v4", "v0"), ("v3", "v4")], "",
        {
            "v0": [("v1", 100, 2), ("v2", 10, 15)],
            "v1": [("v2", 200, 4)],
            "v2": [("v3", 100, 4)],
            "v3": [("v4", 80, 5), ("v5", 100, 1)],
            "v4": [("v5", 10, 1)],
            "v5": [("v0", 75, 1)],

        }
    )
    print(mission_test.temps_affile())
    print()
    print(mission_test.temps_choix())
