import numpy as np
import math
import kayak
from .. import export

try:
    import networkx as nx
    KAYAK_NETWORKX = True
except ImportError:
    KAYAK_NETWORKX = False

if KAYAK_NETWORKX:
    @export
    class ErdosRenyiGraphType(kayak.FeatureType):
        def __init__(self, nodes, connection_probability):
            self._nodes = int(nodes)
            self._prob = float(connection_probability)

        def fits(self, code):
            code_size = len(code)
            nodes = math.sqrt(code_size)
            if nodes % 1 != 0:
                # We have no quadratic code size, so it is no valid adjacency matrix for a graph
                return False
            nodes = int(nodes)  # make sure it is an integer

            if nodes > self._nodes:
                # Graph is too big for this feature type
                return False

            numpy_matrix = np.reshape(np.array(code), [nodes, nodes])
            nx.from_numpy_array(numpy_matrix)
            return True

        def sample_random(self):
            """
            :return:
            :rtype: np.ndarray
            """
            sampled_graph = nx.erdos_renyi_graph(self._nodes, self._prob)
            return nx.to_numpy_array(sampled_graph)

        def cross_over(self, code1, code2):
            """

            :param code1:
            :type code1 kayak.GeneCode|list|numpy.array
            :param code2:
            :type code2 kayak.GeneCode|list|numpy.array
            :return:
            :rtype: kayak.GeneCode
            """
            raise NotImplementedError()

        def __len__(self):
            return self._nodes


    @export
    class DAGraphType(kayak.FeatureType):
        def __init__(self, graph: nx.DiGraph):
            if graph is None:
                raise ValueError('No graph given')

            numpy_matrix = nx.to_numpy_matrix(graph)


        def cross_over(self, code1, code2):
            raise NotImplementedError()

        def _mutate_random(self, code):
            raise NotImplementedError()

        def sample_random(self):
            raise NotImplementedError()

        def fits(self, code):
            raise NotImplementedError()

        def __len__(self):
            raise NotImplementedError()
