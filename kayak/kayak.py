import random
import numpy
import semantic_version
from deprecated import deprecated
from .feature_types import FeatureType
from .feature_types import FeatureSet
from . import export


@export
class GeneticEncoding(FeatureSet):
    """
    Description object for a genetic encoding space based on various feature dimensions which can be manipulated in different ways.
    E.g. there could be one dimension specifying one unique type from a list of given types which can be encoded binary or as integers.
    Operators on such a dimension would provide random uniform sampling or iterating over them (incremeting, decrementing).
    Another feature dimension could be a single float value which could be initialized from various random distributions or mutated by arithmetic operations.
    Feature sets combine multiple dimensions into one feature which is only mutated as a whole.
    They could be nested into hierarchical forms of feature possibilities and let you design pretty arbitrary feature spaces.
    Mutations and mappings determine how you can translate a sampled code from this space into a phenotypical space.
    """

    def __init__(self, name: str, version, feature_description=None):
        if feature_description is None:
            feature_description = {}
        super().__init__(feature_description)

        self._name = name
        try:
            self._version = semantic_version.Version(version)
        except ValueError as e:
            raise ValueError('Invalid semantic version for genetic encoding given', e)

    @deprecated
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

        return self.fits(code)

    def get_dimension(self, name: str):
        return len(self[name])

    @deprecated('Use the GeneticEncoding space as iterable instead')
    def get_ordered_feature_types(self):
        for feature in self._features:
            yield feature['type']

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
        code = []
        code.extend(feature_type.sample_random())
        return code
    else:
        # Unknown type, so it might be a fixed value we return as sample
        return [feature_type]
        # raise NotImplementedError('Unknown feature type for sampling.')


@export
class GeneCode(object):
    """
    A gene is a vector (code) fitting into a certain vector space - its genetic encoding space.
    In addition to a simple numpy array it also provides optimized functionality to access single feature_types of the gene code with respect
    to its genetic encoding space.
    """
    def __init__(self, code, space: FeatureType):
        if not space.fits(code):
            raise ValueError('Code %s does not fit into genetic encoding space %s.' % (code, space))
        self._code = code
        self._space = space

    @deprecated(reason='Kayak by definition will wrap numpy arrays.', version='0.3')
    def as_numpy(self):
        return numpy.array([el.as_numpy() if isinstance(el, GeneCode) else el for el in self._code])

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
        if type(item) is int:
            if item >= len(self._space):
                raise IndexError('Index exceeds number of features in Gene Code.')

            # Count increasing code_index for all ftypes
            return_code = False
            code_offset = 0
            code_length = len(self._code)
            for ftype_idx, ftype in enumerate(self._space):
                # Only count up to ftype_idx which was requested
                if ftype_idx is item:
                    return_code = True

                feature_size = len(ftype)

                if not ftype.dynamically_sized:
                    if return_code:
                        next_subfeature_offset = min(code_offset + feature_size, code_length)
                        subfeature_code = self._code[code_offset:next_subfeature_offset]
                        return ftype.build(subfeature_code)

                    # Fixed-sized ftype lets us simply add its size to jump over its code
                    code_offset += feature_size
                else:
                    check_feature_size = feature_size + 1  # Start with maximum possible size of sub feature
                    subfeature_fits = False
                    while check_feature_size > 0 and not subfeature_fits:
                        next_subfeature_offset = min(code_offset + check_feature_size, code_length)
                        subfeature_code = self._code[code_offset:next_subfeature_offset]
                        if ftype.fits(subfeature_code):
                            subfeature_fits = True
                            if return_code:
                                return ftype.build(subfeature_code)

                            code_offset = next_subfeature_offset  # Update next code offset
                        check_feature_size -= 1  # Decrease feature size to check

        raise ValueError('Accessing non-integer indices not supported.')

    def __str__(self):
        return str(self.as_numpy())

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self._code)