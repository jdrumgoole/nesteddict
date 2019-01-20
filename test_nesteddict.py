"""
Created on 3 May 2017

@author: jdrumgoole

"""

import unittest

from nesteddict import NestedDict


class TestNestedDict(unittest.TestCase):

    def test_init(self):
        x = NestedDict()
        x['a'] = 1
        self.assertEqual(x['a'], 1)

        x = NestedDict({'a': 1, 'b': 2})
        self.assertEqual(x['a'], 1)
        self.assertEqual(x['b'], 2)

        x = NestedDict([("a", 1), ("b", 2)])
        self.assertEqual(x['a'], 1)
        self.assertEqual(x['b'], 2)

        x = NestedDict({("a", 1), ("b", 2)})
        self.assertEqual(x['a'], 1)
        self.assertEqual(x['b'], 2)

        x = NestedDict({'a.b.c': 1, 'x.y.z': 2})
        self.assertEqual(x['a.b.c'], 1)
        self.assertEqual(x['x.y.z'], 2)

        self.assertRaises(ValueError, NestedDict, {7: 1, 'b': 2})
        self.assertRaises(ValueError, NestedDict, {(7, 1), ('b', 2)})
        self.assertRaises(ValueError, NestedDict, [(7, 1), ('b', 2)])

        x = NestedDict({'a.b.c': 1, 'x.y.z': 2}, m=5, n=6)
        self.assertEqual(x['a.b.c'], 1)
        self.assertEqual(x['x.y.z'], 2)
        self.assertEqual(x['m'], 5)
        self.assertEqual(x['n'], 6)

    def test_nesteddict(self):
        x = NestedDict([("a", 1), ("b", 2), ("a.b.c", 3)])
        self.assertTrue("a" in x)
        self.assertTrue("a.b" in x)
        self.assertTrue("a.b.c" in x)
        self.assertEqual(3, x['a.b.c'])
        self.assertEqual(1, x['a'])

    def test_in(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertTrue("a" in x)
        self.assertTrue("a.b" in x)
        self.assertTrue("a" in x)
        self.assertFalse("z" in x)
        self.assertFalse("a.z" in x)

    def test_getitem(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertEqual(x['a'], {"b": 1})
        self.assertEqual(x['a.b'], 1)
        x = NestedDict({'a': {'b': [1, 2, 3]}})
        self.assertEqual(x['a.b'], [1, 2, 3])
        self.assertRaises(KeyError, x.__getitem__, "w.z")

    def test_setitem(self):
        x = NestedDict({"a": {"b": 1}})
        x['c'] = 2
        self.assertEqual(x['c'], 2)
        x['a.b'] = 3
        self.assertEqual(x['a.b'], 3)
        x['a.b.c'] = 6
        x['a.b'] = {'c': 6}

    def test_delitem(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertEqual(x.get('a'), {"b": 1})
        del x['a.b']
        self.assertTrue('a' in x)
        x = NestedDict({"a": {"b": 1}})
        del x['a']
        self.assertFalse('a.b' in x)
        self.assertFalse('a' in x)

    def test_get(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertEqual(x.get('a'), {"b": 1})
        self.assertEqual(x.get('z'), None)
        self.assertEqual(x.get('z', 20), 20)
        self.assertEqual(x.get('a.b'), 1)

    def test_has_key(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertTrue(x.has_key('a'))
        self.assertTrue(x.has_key('a.b'))
        self.assertFalse(x.has_key('z'))

    def test_pop(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertEqual(x.pop('a.b'), 1)
        self.assertFalse("a.b" in x)
        self.assertTrue('a' in x)
        self.assertEqual(x.pop('x.z', 20), 20)

    def test_popitem(self):
        x = NestedDict({"a": {"b": 1}})
        self.assertEqual(x.popitem('a.b'), ('a.b', 1))
        self.assertRaises(KeyError, x.popitem, "x.y")

    def test_valueerror(self):
        x=NestedDict()
        self.assertRaises(ValueError, x.__setitem__, 10, 1)

    def test_update(self):
        x=NestedDict({"a": 1, "b": 2})
        y=NestedDict({"c": 3, "d": 4})
        x.update(y)
        self.assertEqual(len(x), 4)
        self.assertEqual(len(y), 2)
        self.assertEqual(x['a'], 1)
        self.assertEqual(x['b'], 2)
        self.assertEqual(x['c'], 3)
        self.assertEqual(x['d'], 4)

        x=NestedDict({"a": 1, "b": 2})
        y=NestedDict({"c": 3, "d": 4})
        x.update(y, w=10, x=11)
        self.assertEqual(len(x), 6)
        self.assertEqual(len(y), 2)
        self.assertEqual(x['a'], 1)
        self.assertEqual(x['b'], 2)
        self.assertEqual(x['c'], 3)
        self.assertEqual(x['d'], 4)
        self.assertEqual(x['w'], 10)
        self.assertEqual(x['x'], 11)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
