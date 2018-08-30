import unittest
import kayak
import kayak.feature_types as ft

class GeneticEncodingDescriptionTest(unittest.TestCase):
    def test_init(self):
        space = kayak.GeneticEncoding('test', '0.1.0')

    def test_add_feature(self):
        space = kayak.GeneticEncoding('foo', '0.1.1')
        space.add_feature('my_feature', ft.NaturalFloat)

    def test_sample_simple_feature(self):
        space = kayak.GeneticEncoding('foo', '0.1.1')
        space.add_feature('a', ft.NaturalFloat)
        code = space.sample_random()

        self.assertIsInstance(code, kayak.GeneCode)
        self.assertEqual(code.as_numpy().shape, (1,))

    def test_sample_feature(self):
        gene_space3 = kayak.GeneticEncoding('test', '0.1.1')
        gene_space3.add_feature('a', [1, 2, 3])
        gene_space3.add_feature('b', ft.NaturalInteger)
        gene_space3.add_feature('xyz', [
            ft.FeatureSet({'c': [1, 2, 3], 'd': ft.NaturalInteger}),
            ft.FeatureSet({'c': ft.NaturalFloat, 'd': ft.NaturalInteger, 'e': [-1, -2, -3]})
        ])

        code = gene_space3.sample_random()
        self.assertIsInstance(code, kayak.GeneCode)
        print(code.as_numpy())

    def test_mutation_changes(self):
        space = kayak.GeneticEncoding('foo', '0.1.1')
        space.add_feature('a', ft.NaturalFloat)
        space.add_feature('xyz', [
            ft.FeatureSet({'b': [1, 2, 3], 'c': ft.NaturalInteger}),
            ft.FeatureSet({'b': ft.NaturalInteger, 'c': [-1, -2, -3]})
        ])
        code = space.sample_random()

        code.mutate_random(space)

        self.assertIsInstance(code, kayak.GeneCode)
        self.assertEqual(code.as_numpy().shape, (4,))

        print(space.map(code))

