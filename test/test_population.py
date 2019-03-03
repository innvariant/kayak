import unittest
import kayak


class PopulationTest(unittest.TestCase):

    def test_dev(self):
        gen_enc = kayak.GeneticEncoding('test_enc', '0.1.0', {
            'a': kayak.feature_types.natint,
            'b': kayak.feature_types.unitfloat
        })
        pop = kayak.Population(gen_enc)
        pop += 1
        print(pop._pop)

        pop2 = kayak.Population(gen_enc)
        pop2 += 2

        pop += pop2

        print(pop._pop)

    def test_delayed_random_fitness(self):
        gen_enc = kayak.GeneticEncoding('test_enc', '0.1.0', {
            'a': kayak.feature_types.natint,
            'b': kayak.feature_types.unitfloat
        })
        pop = kayak.Population(gen_enc)
        pop += 10

        random_map = kayak.DelayedRandomFitnessMap()

        from multiprocessing.dummy import Pool
        with Pool(4) as pool:
            async_results = [pool.apply_async(random_map.obtain_fitness, args=(code,)) for code in pop]
            try:
                results = [r.get() for r in async_results]
                print(results)
            except StopIteration:
                pass

        for code in pop:
            print('code %s, fitness %s' % (code, random_map.obtain_fitness(code)))
