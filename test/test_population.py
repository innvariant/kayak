import unittest
import kayak


class PopulationTest(unittest.TestCase):

    def test_dev(self):
        gen_enc = kayak.GeneticEncoding('test_enc', '0.1.0', {
            'a': kayak.feature_types.unitfloat,
            'b': kayak.feature_types.unitfloat
        })
        pop = kayak.Population(gen_enc)
        pop += 1
        print(pop._pop)

        pop2 = kayak.Population(gen_enc)
        pop2 += 2

        pop += pop2

        print(pop._pop)
