import unittest
import networkx
import kayak
import kayak.feature_types.graph as fg

class FeatureTypesGraphTest(unittest.TestCase):
    def test_init(self):
        graph = networkx.generators.watts_strogatz_graph(10, 2, 0.6)
        graph_feature = fg.DAGraphType(graph)
