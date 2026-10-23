import unittest

import networkx as nx
import numpy as np

from ast_metric_induction import (
    circular_distances, edge_recovery_metrics, generate_ring_observations,
    infer_top_k_graph, pairwise_gaussian_mi,
)


class TestASTMetricInduction(unittest.TestCase):
    def test_circular_distances(self):
        distances = circular_distances(6)
        self.assertEqual(distances[0, 5], 1)
        self.assertEqual(distances[0, 3], 3)
        np.testing.assert_array_equal(distances, distances.T)

    def test_generation_is_reproducible(self):
        x1, g1 = generate_ring_observations(8, 200, seed=7)
        x2, g2 = generate_ring_observations(8, 200, seed=7)
        np.testing.assert_allclose(x1, x2)
        self.assertEqual(set(g1.edges()), set(g2.edges()))

    def test_planted_graph_is_cycle(self):
        _, graph = generate_ring_observations(8, 100, seed=2)
        self.assertEqual(graph.number_of_nodes(), 8)
        self.assertEqual(graph.number_of_edges(), 8)
        self.assertTrue(nx.is_connected(graph))
        self.assertTrue(all(degree == 2 for _, degree in graph.degree()))

    def test_gaussian_mi_properties(self):
        observations, _ = generate_ring_observations(8, 500, seed=3)
        mi = pairwise_gaussian_mi(observations)
        np.testing.assert_allclose(mi, mi.T)
        self.assertTrue(np.all(mi >= 0))
        np.testing.assert_allclose(np.diag(mi), 0)

    def test_top_k_graph_has_all_nodes(self):
        observations, _ = generate_ring_observations(8, 500, seed=3)
        graph = infer_top_k_graph(pairwise_gaussian_mi(observations), k=2)
        self.assertEqual(graph.number_of_nodes(), 8)
        self.assertGreaterEqual(graph.number_of_edges(), 8)

    def test_perfect_recovery_metrics(self):
        planted = nx.cycle_graph(8)
        metrics = edge_recovery_metrics(planted, planted)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)
        self.assertEqual(metrics["f1"], 1.0)

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            pairwise_gaussian_mi(np.ones((10, 3)))
        with self.assertRaises(ValueError):
            circular_distances(3)


if __name__ == "__main__":
    unittest.main()
