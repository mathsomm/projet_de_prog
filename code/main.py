from network import Network
from graph import Graph
from time import time
from extension import Mission
import heapq
import matplotlib.pyplot as plt
import numpy as np

# Load the network
network_file = "examples/medium-smallfatigue.txt"
network = Network.from_file(network_file)
#print(network.build_extended_graph().shortest_path("lozere", "saclay"))

def benchmark_different_sizes(max_nodes=50, step=5, repetitions=3, loi_log=False):
    sizes = list(range(10, max_nodes + 1, step))
    from math import log10
    if loi_log: 
        B = [k*10**i for i in range(2, int(log10(max_nodes)))  for k in range(1, 10)]
        sizes = [B[step*k] for k in range(0, len(B)//step)]
    results = {
        "simple_graph": [],
        "implicit_graph_no_heuristic": [],
        "implicit_graph_with_heuristic": [],
        "implicit_pareto": [],
        "implicit_pareto_heuristic": []
    }
    
    print("Début du test...")
    print(f"Tailles testées: {sizes}")
    print(f"Répétitions par taille: {repetitions}\n")
    
    for size in sizes:
        print(f"Test avec {size} nœuds...")
        
        times_simple = []
        times_implicit_no_h = []
        times_implicit_h = []
        times_pareto = []
        times_pareto_h = []
        
        for rep in range(repetitions):
            # Créer un graphe aléatoire
            # graphe no fatigue
            g = Network.create_graph(size, distance_range=(10, 100), fatigue_range=(1, 10))
            
            # Test 1: Simple graph
            try:
                t = time()
                g.build_simple_graph().shortest_path(g.start, g.end)
                times_simple.append(time() - t)
            except Exception as e:
                print(f"  ❌ Simple graph failed: {e}")
            
            # Test 2: Implicit graph without heuristic, no pareto
            try:
                t = time()
                g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end, pareto=False)
                times_implicit_no_h.append(time() - t)
            except Exception as e:
                print(f"  ❌ Implicit no heuristic failed: {e}")
            
            # Test 3: Implicit graph with heuristic, no pareto
            try:
                t = time()
                g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end, pareto=False, heuristique=True)
                times_implicit_h.append(time() - t)
            except Exception as e:
                print(f"  ❌ Implicit with heuristic failed: {e}")
            
            # Test 4: Implicit graph with pareto, no heuristic
            try:
                t = time()
                g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end, pareto=True)
                times_pareto.append(time() - t)
            except Exception as e:
                print(f"  ❌ Implicit pareto failed: {e}")
            
            # Test 5: Implicit graph with pareto and heuristic
            try:
                t = time()
                g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end, pareto=True, heuristique=True)
                times_pareto_h.append(time() - t)
            except Exception as e:
                print(f"  ❌ Implicit pareto + heuristic failed: {e}")
        
        # Calculer la moyenne des temps
        if times_simple:
            results["simple_graph"].append(np.mean(times_simple))
        else:
            results["simple_graph"].append(0)
            
        if times_implicit_no_h:
            results["implicit_graph_no_heuristic"].append(np.mean(times_implicit_no_h))
        else:
            results["implicit_graph_no_heuristic"].append(0)
            
        if times_implicit_h:
            results["implicit_graph_with_heuristic"].append(np.mean(times_implicit_h))
        else:
            results["implicit_graph_with_heuristic"].append(0)
            
        if times_pareto:
            results["implicit_pareto"].append(np.mean(times_pareto))
        else:
            results["implicit_pareto"].append(0)
            
        if times_pareto_h:
            results["implicit_pareto_heuristic"].append(np.mean(times_pareto_h))
        else:
            results["implicit_pareto_heuristic"].append(0)
        
        print(f"  ✅ Taille {size}: Simple={results['simple_graph'][-1]:.4f}s, "
              f"Implicit={results['implicit_graph_no_heuristic'][-1]:.4f}s, "
              f"Pareto={results['implicit_pareto'][-1]:.4f}s\n")
    
    return sizes, results

def plot_results(sizes, results):
    """Crée un graphique des résultats de benchmark"""
    plt.figure(figsize=(12, 7))
    
    plt.plot(sizes, results["simple_graph"], marker='o', label="Simple Graph", linewidth=2)
    plt.plot(sizes, results["implicit_graph_no_heuristic"], marker='s', label="Implicit (No Heuristic)", linewidth=2)
    plt.plot(sizes, results["implicit_graph_with_heuristic"], marker='^', label="Implicit (With Heuristic)", linewidth=2)
    plt.plot(sizes, results["implicit_pareto"], marker='d', label="Implicit (Pareto)", linewidth=2)
    plt.plot(sizes, results["implicit_pareto_heuristic"], marker='*', label="Implicit (Pareto + Heuristic)", linewidth=2, markersize=10)
    
    plt.xlabel('Nombre de nœuds', fontsize=12)
    plt.ylabel('Temps (secondes)', fontsize=12)
    plt.title('Benchmark: Temps de calcul du plus court chemin\nselon la taille du graphe', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('benchmark_results.png', dpi=300)
    print("\n📊 Graphique sauvegardé: benchmark_results.png")
    plt.show()

def comparaison_duree():
    g = Network.from_file(network_file)
    
    t = time()
    test = g.build_simple_graph().shortest_path(g.start, g.end)
    print("test simple: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    '''
    t = time()
    test = g.build_extended_graph().shortest_path2(g.start, g.end)[0]
    print("test extended: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end)[0]
    print("test implicite sans rien: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    '''
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=False).shortest_path2(g.start, g.end,pareto=True)[0]
    print("test implicite avec pareto : \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
   
    t = time()
    test = g.build_implicit_graph(précalcul_heuristique=True).shortest_path2(g.start, g.end,pareto=True, heuristique=True)[0]
    print("test implicite avec pareto et heuristique: \n", "temps: ", time()-t, "\n", "resultat: ", test)
    
def test_multitude_missions():
    missions = [("v0", "v5"), ("v5", "v10"), ("v15", "v40"), ("7", "30")]
    m = Mission(missions, network_file)
    #print(m.temps_choix(), "\n--------")
    print(m.temps_affile_2(True))


# Lancer le benchmark
sizes, results = benchmark_different_sizes(max_nodes=1000, step=20, repetitions=100)
plot_results(sizes, results)
#comparaison_duree()
#test_multitude_missions()
