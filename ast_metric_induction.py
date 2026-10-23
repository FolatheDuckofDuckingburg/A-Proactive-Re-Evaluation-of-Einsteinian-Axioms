"""Synthetic graph-recovery benchmark for Assumption Stress Testing (AST).

This is NOT a physical spacetime model. A circular correlation structure is
planted in a Gaussian covariance matrix, sampled, and then recovered from
pairwise Gaussian mutual-information estimates.
"""
import argparse

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def circular_distances(num_nodes):
    if num_nodes < 4:
        raise ValueError("num_nodes must be at least 4")
    idx = np.arange(num_nodes)
    raw = np.abs(idx[:, None] - idx[None, :])
    return np.minimum(raw, num_nodes - raw)


def generate_ring_observations(num_nodes=24, num_samples=4000,
                               length_scale=1.0, seed=42):
    """Return synthetic observations and the known planted ring graph."""
    if num_nodes < 4:
        raise ValueError("num_nodes must be at least 4")
    if num_samples < 20:
        raise ValueError("num_samples must be at least 20")
    if length_scale <= 0:
        raise ValueError("length_scale must be positive")
    distances = circular_distances(num_nodes)
    covariance = np.exp(-distances / length_scale)
    rng = np.random.default_rng(seed)
    observations = rng.multivariate_normal(
        np.zeros(num_nodes), covariance, size=num_samples, check_valid="raise"
    )
    planted = nx.cycle_graph(num_nodes)
    return observations, planted


def pairwise_gaussian_mi(observations):
    """Estimate pairwise MI in nats assuming bivariate Gaussian variables.

    Uses I(X;Y) = -0.5 log(1-r^2), with sample correlation r. This is not a
    general-purpose MI estimator for arbitrary distributions.
    """
    data = np.asarray(observations, dtype=float)
    if data.ndim != 2 or data.shape[0] < 3 or data.shape[1] < 2:
        raise ValueError("observations must be 2D with >=3 rows and >=2 columns")
    if not np.isfinite(data).all():
        raise ValueError("observations must be finite")
    if np.any(np.std(data, axis=0) == 0):
        raise ValueError("each variable must have non-constant observations")
    corr = np.corrcoef(data, rowvar=False)
    corr = np.clip(corr, -1 + 1e-12, 1 - 1e-12)
    mi = -0.5 * np.log1p(-(corr ** 2))
    np.fill_diagonal(mi, 0.0)
    return mi


def infer_top_k_graph(mi, k=2):
    """Connect each node to its k highest-scoring MI neighbours (undirected)."""
    scores = np.asarray(mi, dtype=float)
    if scores.ndim != 2 or scores.shape[0] != scores.shape[1]:
        raise ValueError("mi must be a square matrix")
    n = scores.shape[0]
    if not 1 <= k < n:
        raise ValueError("k must satisfy 1 <= k < number of nodes")
    if not np.isfinite(scores).all():
        raise ValueError("mi must be finite")
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for node in range(n):
        candidates = [j for j in range(n) if j != node]
        for neighbour in sorted(candidates, key=lambda j: scores[node, j],
                                reverse=True)[:k]:
            graph.add_edge(node, neighbour, weight=float(scores[node, neighbour]))
    return graph


def edge_recovery_metrics(inferred, planted):
    """Return edge precision, recall, and F1 against the planted graph."""
    inferred_edges = {tuple(sorted(e)) for e in inferred.edges()}
    planted_edges = {tuple(sorted(e)) for e in planted.edges()}
    tp = len(inferred_edges & planted_edges)
    precision = tp / len(inferred_edges) if inferred_edges else 0.0
    recall = tp / len(planted_edges) if planted_edges else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if precision + recall else 0.0)
    return {"true_positive_edges": tp, "inferred_edges": len(inferred_edges),
            "planted_edges": len(planted_edges), "precision": precision,
            "recall": recall, "f1": f1}


def run_benchmark(num_nodes=24, num_samples=4000, length_scale=1.0,
                  seed=42, plot=True):
    observations, planted = generate_ring_observations(
        num_nodes, num_samples, length_scale, seed
    )
    inferred = infer_top_k_graph(pairwise_gaussian_mi(observations), k=2)
    metrics = edge_recovery_metrics(inferred, planted)
    print("AST synthetic graph-recovery benchmark")
    print("A planted synthetic structure is being recovered; this is not physical evidence.")
    print(f"nodes={num_nodes}, samples={num_samples}, seed={seed}")
    print("precision={precision:.3f}, recall={recall:.3f}, F1={f1:.3f}".format(**metrics))
    if plot:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        pos = nx.circular_layout(planted)
        nx.draw_networkx(planted, pos, ax=axes[0], node_size=180,
                         with_labels=True, font_size=8)
        axes[0].set_title("Planted ring")
        nx.draw_networkx(inferred, pos, ax=axes[1], node_size=180,
                         with_labels=True, font_size=8, edge_color="tab:blue")
        axes[1].set_title("Inferred graph from Gaussian MI ranking")
        for ax in axes:
            ax.axis("off")
        fig.suptitle("Synthetic benchmark only: ring structure is planted in the data")
        fig.tight_layout()
        plt.show()
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=24)
    parser.add_argument("--samples", type=int, default=4000)
    parser.add_argument("--length-scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    run_benchmark(args.nodes, args.samples, args.length_scale, args.seed,
                  plot=not args.no_plot)
