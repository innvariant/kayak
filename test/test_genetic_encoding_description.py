import unittest
import kayak


class GeneticEncodingDescriptionTest(unittest.TestCase):
    def test(self):
        space = kayak.GeneticEncoding('test', '0.1.0')