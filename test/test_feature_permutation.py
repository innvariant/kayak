import unittest
import kayak.feature_types as ft

class FeaturePermutationTest(unittest.TestCase):
    def test_named_construction_success(self):
        # Arrange
        permutation_description = ['A', 'B', 'C', 'D']

        # Act
        feature = ft.FeaturePermutation(permutation_description)
        code = feature.sample_random()

        print(code)
        print(feature.decode(code))

    def test_numeric_range_construction_success(self):
        # Arrange
        length = 8
        permutation_description = '1:%s' % length

        # Act
        feature = ft.FeaturePermutation(permutation_description)
        code = feature.sample_random()

        print(code)
        print(feature.decode(code))
        self.assertEqual(len(feature.decode(code)), length)
