from . import export

@export
class Operation(object):
    def apply(self, value, feature_type):
        raise NotImplementedError()

@export
class RandomMutation(Operation):
    def apply(self, value, feature_type):
        return value