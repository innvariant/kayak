import random
import numpy as np
import kayak

from .. import export


def extract_single_native_value(code):
    try:
        # Given code might be wrapped in a list / numpy array
        size = len(code)
        if size is not 1:
            # We expect a single dimension
            raise ValueError('Expecting a single dimension in code. Got code of size %s' % size)
        else:
            return code[0]
    except TypeError:
        return code


def pythonic_to_object_description(description, order=None):
    if type(description) is dict:
        # {'b': int, 'a': float}, ['a', 'b'] -> FeatureSet({'a': float, 'b': int}, ['a', 'b'])
        new_description = FeatureSet()


@export
class FeatureType(object):
    """
    Interface for generic feature types (instances are no feature_types but type representations).
    The feature type instance decides how to mutate given feature_types (code vectors), sample them randomly or cross them over.
    """

    def cross_over(self, code1, code2):
        """

        :param code1:
        :type code1 kayak.GeneCode|list|numpy.array
        :param code2:
        :type code2 kayak.GeneCode|list|numpy.array
        :return:
        :rtype: kayak.GeneCode
        """
        raise NotImplementedError()

    def mutate_random(self, code):
        """

        :param code:
        :type code list|numpy.array
        :return:
        :rtype: kayak.GeneCode
        """
        '''
        Either this interface method can be directly overwritten to implement the random mutation on a given code or the _mutate_random(code) can be
        used for similar behavious between several classes of feature types.
        '''
        return self._wrap_mutate_random(code)

    def _wrap_mutate_random(self, code):
        """
        Common pre-checking code for a random mutation function of feature type classes. Either implement mutate_random(code) or _mutate_random(code),
        based on your required behaviour.
        """
        if not isinstance(code, np.ndarray):
            code = np.array(code)  # numpy array accepts almost all objects

        if len(self) is not len(code):
            raise ValueError('Can not mutate code which does not fit this feature type!')

        return self._mutate_random(code)

    def _mutate_random(self, code):
        raise NotImplementedError('You have to implement this method for the concrete feature type.')

    def sample_random(self):
        """
        :return:
        :rtype: kayak.GeneCode
        """
        raise NotImplementedError()

    def fits(self, code):
        """

        :param code: numpy array
        :return: whether a code fits into FeatureType
        :rtype: boolean
        """
        raise NotImplementedError()

    def __len__(self):
        """
        :return: Number of dimensions for feature codes sampled from this feature type.
        :rtype: int
        """
        raise NotImplementedError()

    def __repr__(self):
        return str(self)


@export
class FeatureSet(FeatureType):
    """
     A feature containing multiple sub-feature_types within a genetic encoding space.
     Single values of this set can only be mutated together.
    """
    def __init__(self, feature_description, order: list=None):
        """

            ```
            FeatureSet({
                'b': ft.int,
                'a': [ {ft.int, ft.float}, ft.float ],
                'c': [
                    { 'x': ft.int, 'y': ft.float },
                    { 'u': ft.float, 'v': ft.int }
                ]
            })
            ```

            Initializing with a list must not be confused with initializing a feature list!
            ```
            FeatureSet([ft.int, ft.float])  # = FeatureSet({1: ft.int, 2: ft.float}, order=[1,2])
            [ft.int, ft.float]  # = FeatureList([ft.int, ft.float])
            ```

        :param feature_description:
        :param order:
        """
        if type(feature_description) is set:
            raise ValueError('We need a deterministic feature name ordering. You can not initialize feature sets with a simple set.')

        # We can either initialize with a list or a dict
        if type(feature_description) is list:
            # For sets we need to generate keys / feature names and then create the dict out of it
            feature_description = {numeric_key: feature for numeric_key, feature in zip(range(len(feature_description)), feature_description)}

        if order is None:
            order = sorted(feature_description.keys())
        elif set(feature_description.keys()) != set(order):
            raise ValueError('Your order list for your feature names do not match up')

        # Transform each pythonic feature representation into an object-representation
        for name in feature_description:
            ftype = feature_description[name]
            if type(ftype) is list:
                feature_description[name] = FeatureList(ftype)

            elif type(ftype) is dict:
                feature_description[name] = FeatureSet(ftype)

        # Provides O(1) access for positions and provides order of features
        # ['a', 'b', 1]
        # _feature_names[1] -> 'b'
        # _features[_feature_names[1]] -> ftype of 'b'
        self._feature_names = order

        # Provides O(1) access for named features
        # { 'a': ft.int, 'b': ft.float }
        # _features['b'] -> ft.float
        self._features = feature_description

    def has_feature(self, name):
        return name in self._features

    def add_feature(self, name, ftype):
        if self.has_feature(name):
            raise ValueError('Feature with that name already contained.')
        self._feature_names.append(name)
        self._features[name] = ftype

    def __getitem__(self, item):
        if type(item) is int:
            if item >= len(self._feature_names):
                raise IndexError('Index exceeds number of features in set.')
            return self._features[self._feature_names[item]]
        elif item in self._feature_names:
            return self._features[item]
        else:
            raise ValueError('Unknown feature %s' % item)

    def get_features(self):
        # TODO do we want to provide such transparent access? might deprecate
        return self._features

    def _mutate_random(self, code):
        offset = 0
        for name in self._features:
            ftype = self._features[name]
            fsize = len(ftype)
            code[offset:fsize] = ftype.mutate_random(code[offset:len(ftype)])
            offset += fsize

    def generate_random(self, num_samples):
        for idx in range(num_samples):
            yield self.sample_random()

    def sample_random(self):
        code = []
        for name in self._features:
            ftype = self._features[name]
            if isinstance(ftype, list):
                list_choice = random.choice(ftype)
                if isinstance(list_choice, FeatureType):
                    code.extend(list_choice.sample_random())
                else:
                    code.append(list_choice)
            elif isinstance(ftype, FeatureType):
                code.extend(ftype.sample_random())
            else:
                raise ValueError('Unknown type for feature: %s' % ftype)
        return kayak.GeneCode(code, self)

    def fits(self, code):
        subfeature_offset = 0
        code_length = len(code)

        for ftype in self:
            if not isinstance(ftype, FeatureType):
                # We have a native python type, e.g. a string or a number, but not a feature type
                next_subfeature_offset = subfeature_offset + 1
                subfeature_code = code[subfeature_offset:next_subfeature_offset]
                if not subfeature_code == ftype:
                    return False
                subfeature_offset = next_subfeature_offset
            else:
                # We have a feature type which might reserve a certain code size
                # For dynamic feature types (e.g. lists) we must iteratively check different code sizes
                feature_size = len(ftype)

                if feature_size is 1:
                    next_subfeature_offset = subfeature_offset + 1
                    subfeature_code = code[subfeature_offset:next_subfeature_offset]
                    if len(subfeature_code) < 1:
                        return False
                    if not ftype.fits(subfeature_code):
                        return False
                    subfeature_offset = next_subfeature_offset
                else:
                    check_feature_size = feature_size + 1
                    subfeature_fits = False
                    while check_feature_size > 0 and not subfeature_fits:
                        next_subfeature_offset = min(subfeature_offset + check_feature_size, code_length)
                        subfeature_code = code[subfeature_offset:next_subfeature_offset]
                        if ftype.fits(subfeature_code):
                            subfeature_fits = True
                            subfeature_offset = next_subfeature_offset
                        check_feature_size -= 1

                    if not subfeature_fits:
                        return False
        return True

    def __eq__(self, other):
        # TODO implement native equality check
        return str(other) == str(self)

    def __str__(self):
        return '{' + ', '.join([str(feat) for feat in self]) + '}'

    def __len__(self):
        return sum(len(feat) for feat in self)


@export
class IntegerType(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return np.array([random.randint(self._lower_border, self._upper_border)])

    def mutation_difference(self):
        range = round((self._upper_border - self._lower_border) * 0.1)
        return random.randint(-range, range)

    def _mutate_random(self, code):
        mutation = code + self.mutation_difference()
        if mutation > self._upper_border:
            mutation = self._upper_border
        if mutation < self._lower_border:
            mutation = self._lower_border
        return mutation

    def fits(self, code):
        try:
            code = extract_single_native_value(code)
        except ValueError:
            return False

        # Fits must not assert but return False on problematic / non-fitting code.
        return np.issubdtype(type(code), np.signedinteger) and self._lower_border <= code <= self._upper_border

    def __str__(self):
        return 'int(%.2f, %.2f)' % (self._lower_border, self._upper_border)

    def __len__(self):
        return 1


@export
class FloatType(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return np.array([random.uniform(self._lower_border, self._upper_border)])

    def mutation_difference(self):
        sigma = (self._upper_border - self._lower_border) * 0.1
        return random.normalvariate(0, sigma)

    def _mutate_random(self, code):
        mutation = code + self.mutation_difference()
        if mutation > self._upper_border:
            mutation = self._upper_border
        if mutation < self._lower_border:
            mutation = self._lower_border
        return mutation

    def fits(self, code):
        try:
            code = extract_single_native_value(code)
        except ValueError:
            return False
        return self._lower_border <= code <= self._upper_border

    def __str__(self):
        return 'float(%.2f, %.2f)' % (self._lower_border, self._upper_border)

    def __len__(self):
        return 1


@export
class FeatureList(FeatureType):

    def __init__(self, feature_description, encoding=None):
        """
        [
        ft.FeatureSet({'x1': ft.NaturalInteger, 'x2': ft.NaturalInteger}),
        ft.FeatureSet({'x3': ft.NaturalFloat, 'x4': ft.NaturalInteger, 'x5': ft.NaturalFloat})
        ]
        """

        for i in range(len(feature_description)):
            ftype = feature_description[i]
            if type(ftype) is list:
                feature_description[i] = FeatureList(ftype)

            elif type(ftype) is dict:
                feature_description[i] = FeatureSet(ftype)

        if encoding is None:
            self._encoding = encoding_dynamic
        else:
            self._encoding = encoding

        self._features = feature_description

    def __getitem__(self, item):
        if type(item) is int:
            if item >= len(self._features):
                raise IndexError('Index exceeds number of features in set.')
            return self._features[item]

    def cross_over(self, code1, code2):
        pass

    def _mutate_random(self, code):
        pass

    def sample_random(self):
        feature_list = self._features
        encoding = self._encoding

        if encoding == encoding_dynamic:
            list_choice = random.randint(0, len(feature_list) - 1)
            ftype = feature_list[list_choice]
            code = [list_choice]
            if isinstance(ftype, FeatureType):
                code.extend(ftype.sample_random().as_numpy())
            else:
                code.append(ftype)
            return kayak.GeneCode(code, self)

        if encoding == encoding_one_hot:
            #One Hot Encoding
            raise NotImplementedError('The one_hot_encoding option is not implemented.')

        if encoding == encoding_max_option:
            #Maximum Option Encoding
            raise NotImplementedError('The maximum_option_encoding option is not implemented.')

        raise ValueError('Wrong type of encoding.')

    def fits(self, code):
        index = code[0]
        feature = self._features[index]
        code = code[1:]
        if len(code) > len(feature) or not feature.fits(code):
            return False

        return True

    def __len__(self):
        length_list = []
        for feature in self._features:
            length_list.append(len(feature))
        return max(length_list)

    def __str__(self):
        return '[' + ', '.join([str(feat) for feat in self]) + ']'


NaturalInteger = IntegerType(1, 5000)
NaturalFloat = FloatType(1, 100)
UnitFloat = FloatType(0, 1)
natint = NaturalInteger
natfloat = NaturalFloat
unitfloat = FloatType(0, 1)
encoding_one_hot = 'ONE_HOT'
encoding_dynamic = 'DYNAMIC'
encoding_max_option = 'MAX_OPTION'
