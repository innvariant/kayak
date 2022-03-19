import unittest
import kayak
import numpy as np
import time


class MatrixTest(unittest.TestCase):

    def test_dev(self):
        shape = [2, 5]
        gen_enc = kayak.GeneticEncoding('test_enc', '0.1.0', {
            'a': kayak.feature_types.Matrix(*shape),
            'b': kayak.feature_types.unitfloat
        })

        print(time.time())
        sample = gen_enc.sample_random()

        sampled_matrix = sample[0]
        self.assertTrue(all(np.equal(sampled_matrix.shape, shape)))