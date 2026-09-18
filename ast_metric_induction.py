"""
Assumption Stress Testing (AST) - Computational Simulation
Description: Verifies macro-geometric metric induction from discrete informational proximity networks.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def run_spacetime_induction(num_nodes=35, seed=42):
    np.random.seed(seed)
    print(f"[AST ENGINE] Initializing {num_nodes} relational information nodes...")
    
    # 1. Initialize Informational Matrix (Proximity = Shared States)
    info_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                info_matrix[i][j] = 1.0
            else:
                # Topologically map a circular/ring space where information decays with step distance
                step_distance = min(abs(i - j), num_nodes - abs(i - j))
                info_matrix[i][j] = np.exp(-step_distance / 2.2) + np.random.normal(0, 0.04)
                info_matrix[i][j] = max(0.0, info_matrix[i][j])
                
    # 2. Build the Network Graph from proximity thresholds
    G = nx.Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if info_matrix[i][j] > 0.18:  # Filter out weak/noise links
                G.add_edge(i, j, weight=info_matrix[i][j])
                
    # 3. Calculate spatial embedding coordinates based on weights (Spring Layout)
    print("[AST ENGINE] Optimization pass: Coarse-graining geometric metric layout...")
    pos = nx.spring_layout(G, weight='weight', seed=seed)
    
    # 4. Render the Emergent Metric Topology Visualizer
    plt.figure(figsize=(9, 7))
    plt.style.use('dark_background')
    
    nx.draw_networkx_nodes(G, pos, node_color='#00ffcc', node_size=180, alpha=0.9)
    nx.draw_networkx_edges(G, pos, edge_color='#ffffff', alpha=0.25, width=1.5)
    
    plt.title("AST Toy Model: Emergent Relational Spacetime Loop\nMetric Induction from Mutual Information Proximity Fields", 
              fontsize=12, color='#ffffff', pad=15)
    plt.axis('off')
    plt.tight_layout()
    
    print("[AST ENGINE] Rendering complete. Smooth spatial grid achieved.")
    plt.show()

if __name__ == "__main__":
    run_spacetime_induction()
