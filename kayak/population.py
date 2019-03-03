import numpy as np
from .kayak import GeneticEncoding, GeneCode

class Population(object):
    _pop = set()

    def __init__(self, encoding):
        if not isinstance(encoding, GeneticEncoding):
            raise ValueError('Expecting a genetic encoding space description for the population.')

        self._space = encoding

    def add_gene(self, gene_code):
        if not isinstance(gene_code, GeneCode):
            raise ValueError('Expecting valid gene code object fitting in encoding space of this population: type %s' % type(gene_code))
        if not self._space.fits(gene_code):
            raise ValueError('Given gene code does not fit into encoding space of this population.')
        self._pop.add(gene_code)

    def add_population(self, other):
        self._pop = self.merge_population(other)

    def merge_population(self, other):
        assert isinstance(other, Population), 'Expecting other object to add to be a population object, got type %s' % type(other)

        if self._space != other._space:
            raise ValueError('Encoding spaces of populations to merge do not fit')

        return self._pop | other._pop

    def __iadd__(self, other):
        if isinstance(other, Population):
            self.add_population(other)
        else:
            if not type(other) is int:
                raise ValueError('Can not add non-population or non-integer value to population object.')

            for gene in self._space.generate_random(int(other)):
                self.add_gene(gene)
        return self

    def __radd__(self, other):
        return other + len(self)

    def __len__(self):
        return len(self._pop)

    def __iter__(self):
        return iter(self._pop)


class FitnessMap(object):
    def obtain_fitness(self, gene_code):
        raise NotImplementedError('Concrete fitness mapping object for population has to be implemented.')

    def __getitem__(self, item):
        assert isinstance(item, GeneCode), 'Expecting selected item object to be a GeneCode, got type %s' % type(gene_code)
        return self.obtain_fitness(item)


class DelayedRandomFitnessMap(FitnessMap):
    _fitness_map = {}

    def obtain_fitness(self, gene_code):
        if gene_code not in self._fitness_map:
            import time
            time.sleep(np.random.randint(0, 3))
            self._fitness_map[gene_code] = np.random.random()
        return self._fitness_map[gene_code]
