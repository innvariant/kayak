import random
from . import export

@export
class FeatureType(object):
    def cross_over(other_gene):
        raise NotImplementedError()

    def mutate_random(self):
        raise NotImplementedError()

    def sample_random(self):
        raise NotImplementedError()

@export
class FeatureSetType(FeatureType):
    """
     A feature containing multiple sub-features within a genetic encoding space.
     Single values of this set can only be mutated together.
    """
    def __init__(self, features):
        self._features = features

    def get_features(self):
        return self._features

@export
class NaturalFloatFeature(FeatureType):
    def sample_random(self):
        return random.uniform(-100, 100)

@export
class NaturalNumberFeature(FeatureType):
    def sample_random(self):
        return random.randint(1, 5000)

