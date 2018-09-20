import unittest
import kayak
import kayak.feature_types as ft
import numpy

class GeneticEncodingDescriptionTest(unittest.TestCase):
    def test_init_fail(self):
        """
        Constructing a gene code with a space it does not fit in has to raise an exception.
        """

        # Arrange
        space = kayak.GeneticEncoding('test', '1.2.0')

        # Act & Assert
        with self.assertRaises(ValueError):
            kayak.GeneCode(numpy.array([1, 2, 3]), space)

    def test_init_success(self):
        """
        Constructing a gene code with a simple space it should fit in, should work.
        """

        # Arrange
        space = kayak.GeneticEncoding('test', '1.2.0')
        space.add_feature('first', ft.NaturalInteger)
        space.add_feature('second', ft.NaturalInteger)

        # Act
        code = kayak.GeneCode(numpy.array([1, 2]), space)

        # Assert
        self.assertTrue(space.contains(code))

    def test_index_access(self):
        """
        Accessing a kayak.GeneCode instance with numeric indices must return values of the specific dimension of the vector.
        """

        # Arrange
        space = kayak.GeneticEncoding('test', '1.2.0')
        space.add_feature('first', ft.NaturalInteger)
        space.add_feature('second', ft.NaturalInteger)
        code_val_0 = 10
        code_val_1 = 12

        # Act
        code = kayak.GeneCode(numpy.array([code_val_0, code_val_1]), space)
        item_0 = code[0]
        item_1 = code[1]

        # Assert
        self.assertEqual(item_0, code_val_0)
        self.assertEqual(item_1, code_val_1)

    def test_feature_access(self):
        """
        Accessing a kayak.GeneCode instance with feature names must be able to resolve the feature mapping and return only the value or vector for
        the requested feature.
        """

        # Arrange
        space = kayak.GeneticEncoding('test', '1.2.0')
        name_outer = 'outer'
        name_inner1 = 'inner1'
        name_inner2 = 'inner2'
        space.add_feature(name_outer, ft.FeatureSet({
            name_inner1: ft.NaturalInteger,
            name_inner2: ft.NaturalFloat
        }))
        code_val_0 = 10
        code_val_1 = 3.4
        feature_code = numpy.array([code_val_0, code_val_1])

        # Act
        code = kayak.GeneCode(feature_code, space)
        feature_outer = code[name_outer]
        feature_inner1 = code[name_inner1]
        feature_inner2 = code[name_inner2]

        # Assert
        self.assertEqual(feature_outer, feature_code)
        self.assertEqual(feature_inner1, code_val_0)
        self.assertEqual(feature_inner2, code_val_1)