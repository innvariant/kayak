import unittest
import kayak.feature_types as ft


class FeatureListTest(unittest.TestCase):

    def test_sample_feature_list_success(self):
        # Arrange
        feature_list = ft.FeatureList([
            ft.FeatureSet({'x1': ft.NaturalInteger, 'x2': ft.NaturalInteger}),
            ft.FeatureSet({'x3': ft.NaturalFloat, 'x4': ft.NaturalInteger, 'x5': ft.NaturalFloat})
        ])

        # Act
        result = feature_list.sample_random()

        # Assert
        self.assertGreaterEqual(len(result), 2)
        self.assertLessEqual(len(result), 3)

    def test_code_fits_feature_list(self):
        # Arrange
        x = [
            {'a': ft.unitfloat, 'b': ft.natint, 'c': ft.unitfloat},
            {'a': ft.natint, 'b': ft.natint}
        ]
        feature_list = ft.FeatureList(x)

        code = [0, 0.1, 10, 0.1]

        # Act
        result = feature_list.fits(code)

        # Assert
        self.assertTrue(result)

    def test_convert_description_feature_list(self):
        # Arrange
        space_description = [{'a': ft.unitfloat, 'b': ft.natint}]

        # Act
        space = ft.FeatureList(space_description)

        # Assert
        self.assertEqual(len(space), 2)