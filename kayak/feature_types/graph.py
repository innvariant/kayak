from .. import export
import kayak

try:
    import networkx
    KAYAK_NETWORKX = True
except ImportError:
    KAYAK_NETWORKX = False

if KAYAK_NETWORKX:
    @export
    class DAGraphType(kayak.FeatureType):
        def __init__(self, graph: networkx.DiGraph):
            pass

        def cross_over(self, code1, code2):
            raise NotImplementedError()

        def _mutate_random(self, code):
            raise NotImplementedError()

        def sample_random(self):
            raise NotImplementedError()

        def __len__(self):
            raise NotImplementedError()
