import unittest
import dictlistdict
import json
from pathlib import Path
import os

def loadJSON(name, encoding):
    with open(name, "r", encoding=encoding) as input_file:
        return json.load(input_file)


class TestDictListDict(unittest.TestCase):

    def test_GenerateName(self):
        name = "dummy.json"
        namer = dictlistdict.GenerateName(name, ".tst")
        for _ in range(3):
            Path(namer.name()).touch()

        self.assertTrue(os.path.isfile("dummy.tst"))
        self.assertTrue(os.path.isfile("dummy.tst.1"))
        self.assertTrue(os.path.isfile("dummy.tst.2"))
        os.unlink("dummy.tst")
        os.unlink("dummy.tst.1")
        os.unlink("dummy.tst.2")


    def test_dictlistdict_small(self):
        encoding = "Latin-1"

        dictlistdict.json_to_text("small.json", "small.txt")
        dictlistdict.text_to_json("small.txt", "small_new.json")
        orig = loadJSON("small.json", encoding)
        gen = loadJSON("small_new.json", encoding)
        self.assertEqual(orig, gen)


    def test_dictlistdict(self):
        encoding = "Latin-1"

        dictlistdict.json_to_text("cr.json", "cr.txt")
        dictlistdict.text_to_json("cr.txt", "crnew.json")
        orig = loadJSON("cr.json", encoding)
        gen = loadJSON("crnew.json", encoding)
        self.assertEqual(orig, gen)


if __name__ == '__main__':
    unittest.main()
