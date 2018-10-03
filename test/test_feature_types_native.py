import math
import string
import random
import itertools
import unittest
import kayak.feature_types as ft


class FeatureTypeTest(unittest.TestCase):
    def test_sample_size_equals_type_size(self):
        # Arrange
        types = [
            ft.FloatType(-1, 1),
            ft.NaturalFloat,
            ft.NaturalInteger
        ]

        # Act
        for current_type in types:
            code = current_type.sample_random()
            feature_size = len(current_type)

            # Assert
            self.assertEqual(feature_size, len(code))

    def test_lengths(self):
        # Arrange
        base_types = [
            ft.FloatType(-1, 1),
            ft.NaturalFloat,
            ft.NaturalInteger
        ]
        test_lengths = [1, 2, 3, 4, 5, 10, 20, 33, 100]

        for length in test_lengths:
            base_feature_set = {}
            remaining_length = length
            # base_feature_keys = random.sample(string.ascii_lowercase, length)
            base_feature_keys = random.sample([''.join(cs) for cs in itertools.product(string.ascii_lowercase,
                                                                                       repeat=math.ceil(math.log(length,
                                                                                                                 len(
                                                                                                                     string.ascii_lowercase))))],
                                              length)
            while remaining_length > 0:
                use_list_or_base_or_set = random.randint(0, 2)
                feature_name = base_feature_keys.pop()
                if use_list_or_base_or_set is 0:
                    list_length = random.randint(1, remaining_length)
                    base_feature_set[feature_name] = [random.choice(base_types) for _ in range(list_length)]
                    remaining_length -= list_length
                elif use_list_or_base_or_set is 1:
                    base_feature_set[feature_name] = random.choice(base_types)
                    remaining_length -= 1
                else:
                    sub_feature_set = {}
                    sub_feature_set_size = random.randint(1, remaining_length)
                    for no in range(sub_feature_set_size):
                        feature_name = 'f_%s' % no
                        sub_feature_set[feature_name] = random.choice(base_types)
                    base_feature_set[feature_name] = ft.FeatureSet(sub_feature_set)
                    remaining_length -= sub_feature_set_size

            feature_set = ft.FeatureSet(base_feature_set)
            print(base_feature_set)
            print(feature_set)
            print('Expected: %s' % length)
            print('Length is: %s' % len(feature_set))

    def test_sample_float_type(self):
        # Arrange
        ranges = [
            (-1, 1),
            (0, 2),
            (1, 10),
            (-10, -1),
            (-5, 2.5),
            (-3.4, 12.1)
        ]

        # Act
        for range in ranges:
            lr, ur = range
            float_type = ft.FloatType(lr, ur)
            sample = float_type.sample_random()

            # Assert
            self.assertLessEqual(sample, ur)
            self.assertGreaterEqual(sample, lr)

    def test_mutate_float_type(self):
        # Arrange
        limits = [
            (-1, 1),
            (0, 2),
            (1, 10),
            (-10, -1),
            (-5, 2.5),
            (-3.4, 12.1)
        ]
        repetitions = 10

        # Act
        for limit in limits:
            ll, ul = limit
            range_diff = abs(ul - ll)
            float_type = ft.FloatType(ll, ul)
            code = float_type.sample_random()

            for _ in range(repetitions):
                mutation = float_type.mutate_random(code)

                # Assert
                self.assertNotEqual(code, mutation, 'Code and its mutation may not be equal.')
                self.assertLessEqual(mutation, ul)
                self.assertGreaterEqual(mutation, ll)
                self.assertLess(code - mutation, 0.35 * range_diff,
                                'Code and mutation should not differ more than 35% of its possible range space')

    def test_sample_integer_type(self):
        # Arrange
        ranges = [
            (-1, 1),
            (0, 2),
            (1, 10),
            (-10, -1)
        ]

        # Act
        for range in ranges:
            lr, ur = range
            int_type = ft.IntegerType(lr, ur)
            sample = int_type.sample_random()

            # Assert
            self.assertLessEqual(sample, ur)
            self.assertGreaterEqual(sample, lr)

    def test_mutate_integer_type(self):
        # Arrange
        limits = [
            (-1, 1),
            (0, 2),
            (1, 10),
            (-10, -1)
        ]
        repetitions = 100

        # Act
        for limit in limits:
            ll, ul = limit
            range_diff = abs(ul - ll)
            int_type = ft.IntegerType(ll, ul)

            occurances_no_change = 0
            for _ in range(repetitions):
                code = int_type.sample_random()
                mutation = int_type.mutate_random(code)

                # Assert
                if code - mutation < 0.001:
                    # print('Code: %s, mut: %s' % (code, mutation))
                    occurances_no_change += 1
                self.assertLessEqual(mutation, ul)
                self.assertGreaterEqual(mutation, ll)
                self.assertLess(code - mutation, 0.35 * range_diff,
                                'Code and mutation should not differ more than 35% of its possible range space')

            # self.assertLessEqual(occurances_no_change, (2 * repetitions) / range_diff, 'Expecting the number of actual mutations with change to be way more. Possible range diff is %s' % range_diff)

    def test_sample_simple_feature_set(self):
        # Arrange
        sizes = [1, 2, 3, 4, 5, 10]

        # Act
        for size in sizes:
            set_type = _build_feature_set(size,
                                          [ft.UnitFloat, ft.NaturalInteger, ft.NaturalFloat, ft.FloatType(-10, 8)])
            sample = set_type.sample_random()

            # Assert
            print(set_type)
            print(sample)
            print()

    def test_code_fits_IntegerType(self):

        # Arrange
        ranges = [
            (-1, 1),
            (0, 2),
            (1, 10),
            (-10, -1),
            (-5, 2),
            (-3, 12)
        ]

        codes = [
            -1,
            0,
            10,
            -1,
            0,
            11
        ]

        # Act
        for i in range(len(ranges)):
            lr, ur = ranges[i]
            integer_type = ft.IntegerType(lr, ur)
            result = integer_type.fits(codes[i])

            # Assert
            self.assertTrue(result)

    def test_code_fits_FloatType(self):

        # Arrange
        ranges = [
            (-1, 1.5),
            (0, 2),
            (1, 10),
            (-10.6, -1),
            (-5, 2.3),
            (-3.9, 12.5)
        ]

        codes = [
            -1,
            0.1,
            9.9,
            -1.91,
            0,
            11.6
        ]

        # Act
        for i in range(len(ranges)):
            lr, ur = ranges[i]
            float_type = ft.FloatType(lr, ur)
            result = float_type.fits(codes[i])

            # Assert
            self.assertTrue(result)


def _build_feature_set(size, base_types):
    feature_set = {}
    remaining_length = size
    base_feature_keys = random.sample(
        [''.join(cs) for cs in
         itertools.product(string.ascii_lowercase, repeat=math.ceil(math.log(size, len(string.ascii_lowercase))))],
        size
    )

    while remaining_length > 0:
        use_base_or_list_or_set = random.randint(0, 2)
        feature_name = base_feature_keys.pop()
        if use_base_or_list_or_set is 0:
            feature_set[feature_name] = random.choice(base_types)
            remaining_length -= 1
        elif use_base_or_list_or_set is 1:
            list_length = random.randint(1, 10)
            feature_set[feature_name] = [random.choice(base_types) for _ in range(list_length)]
            remaining_length -= 1
        else:
            sub_feature_set_size = random.randint(1, remaining_length)
            sub_feature_set = _build_feature_set(sub_feature_set_size, base_types)
            feature_set[feature_name] = sub_feature_set
            remaining_length -= len(sub_feature_set)

    return ft.FeatureSet(feature_set)
