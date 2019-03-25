import unittest
import kayak.feature_types as ft

class FeatureBundleTest(unittest.TestCase):
    def test_named_construction_success(self):
        # Arrange
        named_feature_bundle_description = {
            'a': ft.unitfloat,
            'b': ft.natint
        }

        # Act
        feature_set = ft.FeatureBundle(named_feature_bundle_description)

        # Assert
        self.assertIsNotNone(feature_set)
        self.assertEqual(len(feature_set), len(named_feature_bundle_description))

    def test_dynamic_sizes_bundle_construction_success(self):
        # Arrange
        named_feature_bundle_description = {
            'a': ft.unitfloat,
            'opts': ft.FeatureOption([
                ft.FeatureBundle({'x1': ft.NaturalInteger, 'x2': ft.NaturalInteger}),
                ft.FeatureBundle({'x3': ft.NaturalFloat, 'x4': ft.NaturalInteger, 'x5': ft.NaturalFloat})
            ])
        }

        # Act
        feature_set = ft.FeatureBundle(named_feature_bundle_description)