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
        An ordered list of features (ordered as it maps the dimensions of the genetic encoding space).
         [
         {'name': 'abc', 'type': ['possible_value_1', 'possible_value_2'], offset: 0},
         {'name': 'xyz', 'type': FeatureSet(), offset: 1},
         {'name': 'tur', 'type': FeatureSet(), offset: 4}
         ]
        """
        self._features = []  # provides O(1) access for positions and provides order of features
        self._features_by_pos = {}  # provides O(1) access by name for position

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
        return self._features

    def _get_dimensions(self, feature):
        required_feature_size = len(feature)  # applies for list or FeatureType

    def sample_random(self):
        code = []
        for feature in self._features:
            feature_name = feature['name']
            feature_type = feature['type']
            offset = feature['offset']

            code.extend(_sample_random_from_feature(feature_type))

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
            map = {**map, **_map_feature(feature['name'], feature['type'], code, feature['offset'])}
        return map


def _map_feature(feature_name, feature_type, code, offset=0):
    feature_size = len(feature_type)
    if isinstance(feature_type, FeatureSet):
        map = {}
        for subfeature_name in feature_type.get_features():
            subfeature_type = feature_type.get_features()[subfeature_name]
            map = {**map, **_map_feature(subfeature_name, subfeature_type, code)}
        return map
    elif isinstance(feature_type, FeatureType):
        return {feature_name: code[offset:feature_size]}
    elif isinstance(feature_type, list):
        return _sample_random_from_feature(random.choice(feature_type))
    else:
        return {}


def _sample_random_from_feature(feature_type):
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
        # TODO Consider providing a one-hot-encoding?
        return _sample_random_from_feature(random.choice(feature_type))
    else:
        # Unknwon type, so it might be a fixed value we return as sample
        return [feature_type]
        # raise NotImplementedError('Unknown feature type for sampling.')

class GeneCode(object):
    def __init__(self, code, space):
        self._code = code
        self._space = space

    def as_numpy(self):
        return numpy.array(self._code)

    def __getitem__(self, item):
        return self._code[item]

    def __str__(self):
        return str(self.as_numpy())