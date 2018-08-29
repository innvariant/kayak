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

    @staticmethod
    def default_sample_random():
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

@export
class NaturalFloat(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return random.uniform(self._lower_border, self._upper_border)

    @staticmethod
    def default_sample_random():
        return random.uniform(-100, 100)

@export
class NaturalNumber(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return random.randint(self._lower_border, self._upper_border)

    @staticmethod
    def default_sample_random():
        return random.randint(1, 5000)

