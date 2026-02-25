import os
import unittest
from hybrid_dict import HybridDict

class TestHybridDict(unittest.TestCase):
    def setUp(self):
        os.system('')
        
    def shortDescription(self):
        doc = super().shortDescription()
        if doc:
            doc = f'\033[32m{doc}\033[0m'
        return doc

    def test_init(self):
        '''Test different ways of constructing a HybridDict'''
        h = HybridDict()
        self.assertEqual(type(h._data), dict)

        h1 = HybridDict({'a':1, 'b':2})
        self.assertEqual(h1.a, 1)
        self.assertEqual(h1.b, 2)

        h2 = HybridDict.fromkeys(["c", "d", "e"])
        self.assertEqual(h2.c, None)
        self.assertEqual(h2.d, None)
        self.assertEqual(h2.e, None)

    def test_accessing(self):
        '''Test different ways of getting and accessing attributes'''
        h = HybridDict()
        h.a = 1
        h["b"] = 2

        self.assertEqual(h['a'], 1)
        self.assertEqual(h.b, 2)

        self.assertEqual('c' not in h, True)
        self.assertEqual('a' in h, True)

    def test_delete(self):
        '''Test deleting an item from the object.'''
        h = HybridDict()
        h.a = 1
        h.b = 2

        self.assertEqual('a' in h, True)
        del h['a']
        self.assertEqual('a' in h, False)

        self.assertEqual('b' in h, True)

    def test_equality(self):
        '''Test equality of two HybridDicts'''
        h = HybridDict()
        h.a = 1
        h.b = 2

        h1 = HybridDict({'a': 1, 'b': 2})
        self.assertEqual(h, h1)

        h2 = HybridDict({'a':0, 'b':0})
        self.assertEqual(h1 == h2, False)

    def test_merging(self):
        '''Test merging two HybridDicts'''
        h = HybridDict()
        h.a = 1
        h.b = 2

        h |= HybridDict({'c':3, 'd':4})

        self.assertEqual(h.c, 3)
        self.assertEqual(h.d, 4)

        h |= HybridDict({'b':7, 'c':5})
        self.assertEqual(h.b, 7)
        self.assertEqual(h.c, 5)
        self.assertEqual(h.a, 1)
        self.assertEqual(h.d, 4)



if __name__ == "__main__":
    unittest.main(verbosity=2)
