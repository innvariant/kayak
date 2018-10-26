import random
import numpy as np
from .. import export


def extract_single_native_value(code):
    try:
        # Given code might be wrapped in a list / numpy array
        size = len(code)
        if size > 1:
            # We expect a single dimension
            raise ValueError('Expecting a single dimension in code')
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
            raise ValueError('Can not mutate code which does not fit this set type!')

        return self._mutate_random(code)

    def _mutate_random(self, code):
        raise NotImplementedError('You have to implement this method for the concrete feature type.')

    def sample_random(self):
        """

        :param code:
        :type code kayak.GeneCode|list|numpy.array
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


@export
class FeatureSet(FeatureType):
    """
     A feature containing multiple sub-feature_types within a genetic encoding space.
     Single values of this set can only be mutated together.
    """
    def __init__(self, feature_description, order:list=None):
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

        :param feature_description:
        :param order:
        """
        if order is None:
            order = sorted(feature_description.keys())
        elif set(feature_description.keys()) != set(order):
            raise ValueError('Your order list for your feature names do not match up')

        self._feature_names = order
        self._features = feature_description

    def get_features(self):
        return self._features

    def _mutate_random(self, code):
        offset = 0
        for name in self._features:
            ftype = self._features[name]
            fsize = len(ftype)
            code[offset:fsize] = ftype.mutate_random(code[offset:len(ftype)])
            offset += fsize

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
        return code

    def fits(self, code):
        subfeatures = self.get_features()
        subfeature_offset = 0
        code_length = len(code)

        for name in subfeatures:
            ftype = subfeatures[name]
            size = len(ftype)

            next_subfeature_offset = subfeature_offset + size
            if code_length < next_subfeature_offset:
                # The current subfeature does not fit into the remaining code length anymore
                return False

            subfeature_code = code[subfeature_offset:next_subfeature_offset]
            if not ftype.fits(subfeature_code):
                # The current code slice does not fit the expected feature type
                return False

            subfeature_offset = next_subfeature_offset

        return True

    def __str__(self):
        return 'featureset[' + ','.join([str(self._features[n]) for n in self._features]) + ']'

    def __len__(self):
        return sum(len(self._features[name]) for name in self._features)


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
        return type(code) == int and self._lower_border <= code <= self._upper_border

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


NaturalInteger = IntegerType(1, 5000)
NaturalFloat = FloatType(1, 100)
UnitFloat = FloatType(0, 1)
int = IntegerType
float = FloatType
natint = NaturalInteger
natfloat = NaturalFloat