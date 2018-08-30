import random
from . import export

@export
class FeatureType(object):
    def cross_over(self, code1, code2):
        raise NotImplementedError()

    def mutate_random(self, code):
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
        '''
         {
          'a': ft.NaturalInt,
          'b': ft.FeatureSet({
           'x': ft.NaturalFloat,
           'y': [1, 2, 3]
          }),
          [
           ft.NaturalInt,
           ft.FeatureSet({'i': ft.NaturalFloat, 'j': ft.NaturalInt })
          ]
         }
        '''

    def get_features(self):
        return self._features

    def cross_over(self, code1, code2):
        raise NotImplementedError()

    def mutate_random(self, code):
        if len(self) is not len(code):
            raise ValueError('Can not mutate code which does not fit this set type!')
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

    def __str__(self):
        return 'featureset[' + ','.join([str(self._features[n]) for n in self._features]) + ']'

    def __len__(self):
        return sum(len(self._features[name]) for name in self._features)


@export
class FloatType(FeatureType):
    def __init__(self, lower_border, upper_border):
        self._lower_border = lower_border
        self._upper_border = upper_border

    def sample_random(self):
        return [random.uniform(self._lower_border, self._upper_border)]

    def mutation_difference(self):
        sigma = (self._upper_border - self._lower_border) * 0.1
        return random.normalvariate(0, sigma)

    def mutate_random(self, code):
        mutation = code + self.mutation_difference()
        if mutation > self._upper_border:
            mutation = self._upper_border
        if mutation < self._lower_border:
            mutation = self._lower_border
        return mutation

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
        return [random.randint(self._lower_border, self._upper_border)]

    def mutation_difference(self):
        range = round((self._upper_border - self._lower_border) * 0.1)
        return random.randint(-range, range)

    def mutate_random(self, code):
        mutation = code + self.mutation_difference()
        if mutation > self._upper_border:
            mutation = self._upper_border
        if mutation < self._lower_border:
            mutation = self._lower_border
        return mutation

    def __str__(self):
        return 'int(%.2f, %.2f)' % (self._lower_border, self._upper_border)

    def __len__(self):
        return 1


NaturalInteger = IntegerType(1, 5000)
NaturalFloat = FloatType(1, 100)
UnitFloat = FloatType(0, 1)