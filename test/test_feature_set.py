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

    def test_simple_code_fits_unnamed_set_success(self):
        # Arrange
        feature_set_description = [ft.natint, ft.natfloat]
        code = [5, 3.8]
        feature_set = ft.FeatureSet(feature_set_description)

        # Act
        fits = feature_set.fits(code)

        # Assert
        self.assertTrue(fits)

    def test_simple_code_fits_named_set_success(self):
        # Arrange
        # Note that y and x are not alphabetically sorted, but the code must still fit for default behaviour
        feature_set_description = {'y': ft.natint, 'x': ft.natfloat}
        code = [3.8, 5]
        feature_set = ft.FeatureSet(feature_set_description)

        # Act
        fits = feature_set.fits(code)

        # Assert
        self.assertTrue(fits)

    def test_set_iteration_default_success(self):
        """
        An unsorted feature set description with names (given a dict) should result in an alphabetically
        sorted FeatureSet object which is iterable.
        """
        # Arrange: a non-alphabetically-ordered set description
        set_description = {
            'y': ft.natfloat,
            'x': ft.unitfloat,
            'a': ft.natint,
            'b': ft.natfloat
        }
        feature_set = ft.FeatureSet(set_description)

        expected_ordered_feature_list = [set_description[name] for name in sorted(set_description.keys())]

        # Act
        iteration_list = [feature for feature in feature_set]

        # Assert
        self.assertListEqual(expected_ordered_feature_list, iteration_list)

    def test_set_iteration_custom_success(self):
        # Arrange: a non-alphabetically-ordered set description
        set_description = {
            'y': ft.natfloat,
            'x': ft.unitfloat,
            'a': ft.natint,
            'b': ft.natfloat
        }
        set_order = ['b', 'a', 'y', 'x']
        feature_set = ft.FeatureSet(set_description, order=set_order)

        expected_feature_list = [set_description[name] for name in set_order]

        # Act
        iteration_list = [feature for feature in feature_set]

        # Assert
        self.assertListEqual(expected_feature_list, iteration_list)

    def test_nested_code_fits_success(self):
        # Arrange
        # Note that the descr is not alphabetically sorted, but the code must still fit for default behaviour
        feature_set_description = {
            'y': ft.natint,
            'a': [ft.unitfloat, ft.natint],
            'x': ft.natfloat
        }
        codes = [
            [0, 0.1, 3.8, 5],
            [1, 10, 4.3, 20],
            [0, 0.9, 12.2, 100]
        ]
        feature_set = ft.FeatureSet(feature_set_description)

        for code in codes:
            # Act
            fits = feature_set.fits(code)

            # Assert
            self.assertTrue(fits, 'Code %s fits not in %s' % (code, feature_set_description))