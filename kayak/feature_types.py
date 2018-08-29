import random
from . import export

@export
class FeatureType(object):
    def cross_over(self, other_gene):
        raise NotImplementedError()

    def mutate_random(self):
        raise NotImplementedError()

    def sample_random(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


@export
class FeatureSet(FeatureType):
    """
     A feature containing multiple sub-features within a genetic encoding space.
     Single values of this set can only be mutated together.
    """
    def __init__(self, features):
        self._features = features

    def get_features(self):
        return self._features

    def __str__(self):
        return 'set(' + ''.join(self._features) + ')'

    def __len__(self):
        return sum(len(f) for f in self._features)


@export
class FloatType(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return random.uniform(self._lower_border, self._upper_border)

    def __str__(self):
        return 'float(%.2f, %.2f)' % (self._lower_border, self._upper_border)

    def __len__(self):
        return 1


@export
class IntegerType(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return random.randint(self._lower_border, self._upper_border)

    def __str__(self):
        return 'int(%.2f, %.2f)' % (self._lower_border, self._upper_border)

    def __len__(self):
        return 1


NaturalInteger = IntegerType(1, 5000)
NaturalFloat = FloatType(1, 100)
UnitFloat = FloatType(0, 1)