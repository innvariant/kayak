import random
import numpy
import semantic_version
from .feature_types import FeatureType
from .feature_types import FeatureSet
from . import export

@export
class GeneticEncoding(object):
    """
    Description object for a genetic encoding space based on various feature dimensions which can be manipulated in different ways.
    E.g. there could be one dimension specifying one unique type from a list of given types which can be encoded binary or as integers.
    Operators on such a dimension would provide random uniform sampling or iterating over them (incremeting, decrementing).
    Another feature dimension could be a single float value which could be initialized from various random distributions or mutated by arithmetic operations.
    Feature sets combine multiple dimensions into one feature which is only mutated as a whole.
    They could be nested into hierarchical forms of feature possibilities and let you design pretty arbitrary feature spaces.
    Mutations and mappings determine how you can translate a sampled code from this space into a phenotypical space.
    """

    def __init__(self, name: str, version):
        self._name = name
        try:
            self._version = semantic_version.Version(version)
        except ValueError as e:
            raise ValueError('Invalid semantic version for genetic encoding given', e)

        """
        An ordered list of feature_types (ordered as it maps the dimensions of the genetic encoding space).
         [
         {'name': 'abc', 'type': ['possible_value_1', 'possible_value_2'], offset: 0},
         {'name': 'def', 'type': ft.UnitFloat, offset: 1},
         {'name': 'xyz', 'type': [FeatureSet({'a': ft.NaturalInteger, 'b': ft.NaturalInteger}), FeatureSet({'a': ft.NaturalInteger)], offset: 2},
         {'name': 'tur', 'type': FeatureSet(), offset: 5}
         ]
        """
        self._features = []  # provides O(1) access for positions and provides order of feature_types
        self._features_by_pos = {}  # provides O(1) access by name for position

    def contains(self, code):
        """
        Checks if the given code fits into this genetic encoding space.

        :param code: Might be a GeneCode, numpy array or a list.
        :return: Flag, indicating if it fits or not.
        :rtype: bool
        """
        if isinstance(code, GeneCode):
            # Unwrap the code if it is contained within a GeneCode object.
            return self.contains(code.as_numpy())

        # TODO implement
        pass

    def add_feature(self, name: str, feature):
        if self.has_feature(name):
            raise ValueError('Feature with that name was already added.')
        next_position = len(self._features)
        previous_feature = self._features[-1] if len(self._features) > 0 else None
        next_offset = previous_feature['offset'] + len(previous_feature['type']) if previous_feature is not None else 0
        one_hot_encoding = any(hasattr(f, '__len__') and len(f) > 1 for f in feature) if len(feature) > 1 else False
        self._features.append({'name': name, 'type': feature, 'offset': next_offset, 'one_hot': one_hot_encoding})
        self._features_by_pos = {name: next_position}

    def has_feature(self, name: str):
        return name in self._features_by_pos

    def get_dimension(self, name: str):
        return self._features_by_pos[name]

    def get_ordered_feature_types(self):
        for feature in self._features:
            yield feature['type']

    def _get_dimensions(self, feature):
        required_feature_size = len(feature)  # applies for list or FeatureType

    def sample_random(self):
        code = []
        for feature in self._features:
            feature_name = feature['name']
            feature_type = feature['type']
            offset = feature['offset']
            one_hot = feature['one_hot']

            code.extend(_sample_random_from_feature(feature_type, one_hot=one_hot))

        return GeneCode(code, self)

    def map(self, code, type_check=False):
        print('Code: ', code)
        print('Features: ', self._features)
        print()
        map = {}
        code_offset = 0
        #for feature in self._features:
        #    feature_size = len(feature['type'])
        #    map[feature['name']] = code[code_offset:feature_size]
        for feature in self._features:
            print(feature)
            print(feature['type'])
            print(feature['offset'])
            map = {**map, **_map_feature(feature['name'], feature['type'], code, feature['offset'], feature['one_hot'])}
            print()
        return map


def _map_feature(feature_name, feature_type, code, offset=0, one_hot=False):
    feature_size = len(feature_type)
    if isinstance(feature_type, FeatureSet):
        map = {}
        subfeature_offset = offset
        for subfeature_name in feature_type.get_features():
            subfeature_type = feature_type.get_features()[subfeature_name]
            subfeature_size = len(subfeature_type)
            if isinstance(subfeature_type, list):
                one_hot_encoding = any(hasattr(f, '__len__') and len(f) > 1 for f in subfeature_type) if len(subfeature_type) > 1 else False
            map = {**map, **_map_feature(subfeature_name, subfeature_type, code, subfeature_offset, one_hot)}
            subfeature_offset += subfeature_size
        return map
    elif isinstance(feature_type, FeatureType):
        value = code[offset:feature_size] if feature_size > 1 else code[offset]
        return {feature_name: value}
    elif isinstance(feature_type, list):
        if one_hot:
            list_choice = code[offset]
            print(list_choice)
            offset += 1
            return {feature_name: list_choice, **_map_feature(feature_name, feature_type[list_choice], code, offset, False)}
        else:
            return {feature_name: code[offset]}
    else:
        return {}


def _sample_random_from_feature(feature_type, one_hot=False):
    if type(feature_type) is type and issubclass(feature_type, FeatureType):
        raise ValueError('Expecting an instance of FeatureType, not the class.')
    elif isinstance(feature_type, FeatureSet):
        code = []
        for subfeature_name in feature_type.get_features():
            subfeature_type = feature_type.get_features()[subfeature_name]
            code.extend(_sample_random_from_feature(subfeature_type))
        return code
    elif isinstance(feature_type, FeatureType):
        return [feature_type.sample_random()]
    elif isinstance(feature_type, list):
        if one_hot:
            list_choice = random.randint(0, len(feature_type) - 1)
            code = [list_choice]
            code.extend(_sample_random_from_feature(feature_type[list_choice]))
            return code
        else:
            return _sample_random_from_feature(random.choice(feature_type))
    else:
        # Unknwon type, so it might be a fixed value we return as sample
        return [feature_type]
        # raise NotImplementedError('Unknown feature type for sampling.')


class GeneCode(object):
    """
    A gene is a vector (code) fitting into a certain vector space - its genetic encoding space.
    In addition to a simple numpy array it also provides optimized functionality to access single feature_types of the gene code with respect
    to its genetic encoding space.
    """
    def __init__(self, code, space: GeneticEncoding):
        if not space.contains(code):
            raise ValueError('Code does not fit into genetic encoding space.')
        self._code = code
        self._space = space

    def as_numpy(self):
        return numpy.array(self._code)

    def assign(self, space: GeneticEncoding):
        """
        Setter method for injecting a genetic encoding space.

        :param space: A fitting genetic encoding space in which space.contains(code) is True.
        :return:
        """
        self._space = space
        return self

    def mutate_random(self):
        print('mutate_random()')
        offset = 0
        for feature in self._space.get_ordered_feature_types():
            feature_size = len(feature)
            if isinstance(feature, FeatureType):
                self._code[offset] = feature.mutate_random(self._code[offset])
            elif isinstance(feature, list):
                print(random.choice(feature))
            else:
                raise ValueError('Unknown feature type')
        print(' -- mutate_random')

    def __getitem__(self, item):
        print(item)
        return self._code[item]

    def __str__(self):
        return str(self.as_numpy())