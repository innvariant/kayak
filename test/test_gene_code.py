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
