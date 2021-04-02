import unittest
from Trie import Trie
import json
with open("TrieTest.json") as fp:
    data = json.load(fp)


class TrieTest(unittest.TestCase):
    def test_insert(self):
        global data
        t = Trie()
        t.insert("Abcd", 23)
        t.insert("Abc", 2)
        t.insert("Xmlnyz", 3)
        t.insert("Xmlnyz", 9)
        t.insert("Xmlny", 10)
        t.insert("Xmlmy", 2)
        json_trie = json.dumps(t.root)
        self.assertTrue(json_trie == json.dumps(data[0]))

    def test_delete(self):
        global data
        t = Trie()
        t.insert("Abcd", 23)
        t.insert("Abc", 2)
        t.insert("Xmlnyz", 3)
        t.insert("Xmlnyz", 9)
        t.insert("Xmlny", 10)
        t.insert("Xmlmy", 2)
        t.delete("Xmlnyz", 9)
        t.delete("Xmlny", 10)
        json_trie = json.dumps(t.root)
        self.assertTrue(json_trie == json.dumps(data[1]))

    def test_courses_containing_word(self):
        global data
        t = Trie()
        t.insert("Abcd", 23)
        t.insert("Abcd", 1)
        t.insert("Abcd", 1)
        t.insert("Abcd", 5)
        t.insert("Abc", 2)
        t.insert("Xmlnyz", 3)
        t.insert("Xmlnyz", 9)
        t.insert("Xmlny", 10)
        t.insert("Xmlmy", 2)
        t.delete("Xmlnyz", 9)
        t.delete("Xmlny", 10)
        self.assertTrue(t.courses_containing_word("Abcd") == {23: 1, 1: 2, 5: 1})
        self.assertTrue(t.courses_containing_word("Xmlnyz") == {3: 1})
        t.delete("Xmlnyz", 3)
        self.assertTrue(t.courses_containing_word("Xmlnyz") == {})


if __name__ == '__main__':
    unittest.main()
