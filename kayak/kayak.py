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
        next_offset = previous_feature['offset'] + len(previous_feature) if previous_feature is not None else 0
        self._features.append({'name': name, 'type': feature, 'offset': next_offset})
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

            if issubclass(feature_type, FeatureType):
                code.append(feature_type.default_sample_random())
            elif isinstance(feature_type, FeatureSet):
                subfeatures = feature_type.get_features()
                pass
            elif isinstance(feature_type, FeatureType):
                code.append(feature_type.sample_random())
            elif isinstance(feature_type, list):
                pass
            else:
                raise NotImplementedError('Unknown feature type for sampling.')

        return GeneCode(code, self)

class GeneCode(object):
    def __init__(self, code, space):
        self._code = code
        self._space = space

    def as_numpy(self):
        return numpy.array(self._code)