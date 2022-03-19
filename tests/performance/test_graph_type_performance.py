import time
import numpy as np
import itertools
import unittest
import networkx as nx
import kayak.feature_types as ft
import kayak.feature_types.graph as fg


class GraphTypePerformanceTest(unittest.TestCase):
    def test_fits_timing(self):
        # Arrange
        graph_sizes = np.arange(500, 5500, 500)
        connection_probabilities = np.arange(0.1, 1, 0.2)

        for prob, graph_size in itertools.product(connection_probabilities, graph_sizes):
            feature_set_description = {
                'a': ft.natint,
                'b': fg.ErdosRenyiGraphType(graph_size, prob),
                'c': ft.unitfloat
            }
            feature_set = ft.FeatureSet(feature_set_description)
            time_generation_start = time.perf_counter()
            generated_graph = nx.erdos_renyi_graph(graph_size, prob)
            time_generation_end = time.perf_counter()
            time_generation_delta = time_generation_end - time_generation_start
            graph_code = nx.to_numpy_array(generated_graph).flatten()
            code = [12]
            code.extend(graph_code)
            code.extend([0.4])

            # Act
            time_fits_start = time.perf_counter()
            fits = feature_set.fits(code)
            time_fits_end = time.perf_counter()

            time_fits_delta = time_fits_end - time_fits_start
            print("\t%sx%.2f - %.6f (gen %.6f)" % (graph_size, prob, time_fits_delta, time_generation_delta))

            # Assert
            self.assertTrue(fits)
            self.assertGreater(time_fits_delta, 0)