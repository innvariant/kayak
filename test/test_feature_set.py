import unittest
import kayak.feature_types as ft


class FeatureSetTest(unittest.TestCase):
    def test_named_construction_success(self):
        # Arrange
        named_feature_set_description = {
            'a': ft.unitfloat,
            'b': ft.natint
        }

        # Act
        feature_set = ft.FeatureSet(named_feature_set_description)

        # Assert
        self.assertIsNotNone(feature_set)
        self.assertEqual(len(feature_set), len(named_feature_set_description))

    def test_unnamed_construction_success(self):
        # Arrange
        unnamed_feature_set_description = [
            ft.natfloat,
            ft.natint,
            ft.NaturalInteger
        ]

        # Act
        feature_set = ft.FeatureSet(unnamed_feature_set_description)

        self.assertIsNotNone(feature_set)
        self.assertEqual(len(feature_set), len(unnamed_feature_set_description))

    def test_unallowed_set_construction_fail(self):
        # Arrange
        unallowed_set_description = {
            ft.FloatType(-1000, 1000),
            ft.IntegerType(0, 500)
        }

        # Act & Assert
        with self.assertRaises(ValueError):
            ft.FeatureSet(unallowed_set_description)

    def test_simple_code_fits_success(self):
        # Arrange
        feature_set_description = [ft.natint, ft.natfloat]
        code = [5, 3.8]
        feature_set = ft.FeatureSet(feature_set_description)

        # Act
        fits = feature_set.fits(code)

        # Assert
        self.assertTrue(fits)