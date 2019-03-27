import math
import random
import numpy as np
import kayak
import itertools

from kayak import FeatureType
from .. import export

@export
class PermutationEncoder(object):
    @staticmethod
    def create(permutation_description):
        raise NotImplementedError('Concrete Encoder has to implement this.')

    @property
    def version(self):
        raise NotImplementedError('Concrete Encoder has to implement this.')

    def decode(self, encoded_permutation):
        raise NotImplementedError('Concrete Encoder has to implement this.')

    def encode(self, explicit_permutation):
        raise NotImplementedError('Concrete Encoder has to implement this.')

    @property
    def encoded_length(self):
        """

        :return: Length of encoded permutation, e.g. 1 for s.th. like code 1234
        :rtype: int
        """
        raise NotImplementedError('Concrete Encoder has to implement this.')

    @property
    def decoded_length(self):
        """
        Actual permutation length, e.g. for three possible values ["A", "B", "C"] this function returns 3.

        :return: Length of permutation (decoded version).
        :rtype: int
        """
        raise NotImplementedError('Concrete Encoder has to implement this.')

    def __str__(self):
        raise NotImplementedError('Concrete Encoder has to implement this.')

    def __len__(self):
        """
        Returns **encoded** permutation length.
        This is more relevant for the concrete encoder as this may vary for the same permutation with same length.
        :return:
        """
        return self.decoded_length

@export
class ExplicitListPermutationEncoder(PermutationEncoder):
    @staticmethod
    def create(permutation_description):
        return ExplicitListPermutationEncoder(permutation_description)

    def __init__(self, description:list):
        """
        ['A', 'B', 'C', 'D']
        :param description:
        """
        self._default_permutation = description

    def decode(self, encoded_permutation):
        return encoded_permutation

    def encode(self, decoded_permutation):
        return decoded_permutation

    def sample_random(self):
        # Fisher-Yates Shuffle
        # https://gist.github.com/JenkinsDev/1e4bff898c72ec55df6f
        permut = list(self._default_permutation)
        random.shuffle(permut)
        return permut

    @property
    def encoded_length(self):
        return len(self._default_permutation)

    @property
    def decoded_length(self):
        return len(self._default_permutation)

    @property
    def version(self):
        return 1

    def fits(self, code):
        return len(code) is self.decoded_length

    def __str__(self):
        return "ExplicitListPermutationEncoder"


@export
class ImplicitListPermutationEncoder(PermutationEncoder):
    @staticmethod
    def create(permutation_description):
        return ImplicitListPermutationEncoder(permutation_description)

    def __init__(self, description:list):
        """
        ['A', 'B', 'C', 'D']
        :param description:
        """
        self._default_permutation = description

    def decode(self, encoded_permutation):
        # TODO can we solve this more efficient?
        last_permut = None
        for _, permut in zip(range(encoded_permutation + 1), itertools.permutations(self._default_permutation)):
            last_permut = permut
        return last_permut

    def sample_random(self):
        possible_codings = math.factorial(self.decoded_length)
        return np.random.randint(possible_codings)

    @property
    def encoded_length(self):
        return 1

    @property
    def decoded_length(self):
        return len(self._default_permutation)

    @property
    def version(self):
        return 1

    def fits(self, code):
        return np.issubdtype(type(code), np.signedinteger)

    def __str__(self):
        return "ListPermutationEncoder"

@export
class RangePermutationEncoder(PermutationEncoder):
    """
    '1:10'
    'A:E'
    """
    @staticmethod
    def create(permutation_description):
        parts = permutation_description.split(':')
        assert len(parts) is 2
        return RangePermutationEncoder(int(parts[0]), int(parts[1]))

    def __init__(self, range_start:int, range_end:int):
        """
        1:10
        :param description:
        """
        self._range_start = range_start
        self._range_end = range_end
        self._default_permutation = range(range_start, range_end + 1)

    def decode(self, encoded_permutation):
        # TODO can we solve this more efficient?
        last_permut = None
        for _, permut in zip(range(encoded_permutation + 1), itertools.permutations(self._default_permutation)):
            last_permut = permut
        return last_permut

    def sample_random(self):
        possible_codings = math.factorial(self.decoded_length)
        return np.random.randint(possible_codings)

    @property
    def encoded_length(self):
        return 1

    @property
    def decoded_length(self):
        return len(self._default_permutation)

    @property
    def version(self):
        return 1

    def fits(self, code):
        return np.issubdtype(type(code), np.signedinteger)

    def __str__(self):
        return "ListPermutationEncoder"

@export
class FeaturePermutation(FeatureType):
    def __init__(self, permutation_description, encoder=None):
        """
        [1, 3, 5, 9], ListPermutationEncoder
        ['A', 'B', 'C', 'D'], ListPermutationEncoder
        '1:10', RangePermutationEncoder
        'A:E', RangePermutationEncoder
        """
        if encoder is None:
            # Resolve encoder automatically
            if type(permutation_description) is list:
                encoder = ExplicitListPermutationEncoder
            elif type(permutation_description) is str:
                if ':' in permutation_description:
                    encoder = RangePermutationEncoder

        if encoder is None:
            raise ValueError('Could not find appropriate encoder for permutation %s' % permutation_description)

        self._encoder = encoder.create(permutation_description)

    def sample_random(self):
        return kayak.GeneCode(np.array([self._encoder.sample_random()]), self)

    def decode(self, code):
        return self._encoder.decode(code[0])

    def fits(self, code):
        return self._encoder.fits(code[0])
