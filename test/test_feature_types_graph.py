import unittest
import networkx as nx
import kayak
import kayak.feature_types as ft
import kayak.feature_types.graph as fg

class FeatureTypesGraphTest(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(fg.ErdosRenyiGraphType(10, 0.3))

    def test_sample_random(self):
        # Arrange
        graph_size = 10
        graph_feature = fg.ErdosRenyiGraphType(10, 0.3)

        # Act
        sampled_graph = graph_feature.sample_random()

        # Assert
        self.assertIsNotNone(sampled_graph)
        self.assertTrue(hasattr(sampled_graph, 'shape'))
        self.assertEqual(len(sampled_graph.shape), 2)  # must be two-dimensional adjacency matrix
        self.assertEqual(sampled_graph.shape[0], sampled_graph.shape[1])  # must be quadratic
        self.assertEqual(sampled_graph.shape[0], graph_size)

    def test_generated_graph_fits_type(self):
        # Arrange
        graph_size = 10
        connection_probability = 0.2
        graph_feature = fg.ErdosRenyiGraphType(graph_size, connection_probability)
        generated_graph = nx.erdos_renyi_graph(graph_size, connection_probability)
        code = nx.to_numpy_array(generated_graph).flatten()

        # Act
        fits = graph_feature.fits(code)

        # Assert
        self.assertTrue(fits)

    def test_graph_in_feature_set(self):
        # Arrange
        graph_size = 10
        connection_probability = 0.2
        feature_set_description = {
            'a': ft.natint,
            'b': fg.ErdosRenyiGraphType(graph_size, connection_probability),
            'c': ft.unitfloat
        }
        feature_set = ft.FeatureSet(feature_set_description)
        generated_graph = nx.erdos_renyi_graph(graph_size, connection_probability)
        graph_code = nx.to_numpy_array(generated_graph).flatten()
        code = [12]
        code.extend(graph_code)
        code.extend([0.4])

        # Act
        fits = feature_set.fits(code)

        # Assert
        self.assertTrue(fits)