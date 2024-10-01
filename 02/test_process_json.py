from unittest import TestCase

from process_json import find_suitable_keys, process_value, process_json


class UnorderedList(list):
    def __eq__(self, other):
        return all([i in other for i in self])


class TestFindSuitableKeys(TestCase):
    def test_empty_result(self):
        d = {"key1": "Word1 word2", "key2": "word2 word3"}
        required_keys = {'keY1', 'Key2'}
        self.assertEqual([], find_suitable_keys(d, required_keys))

    def test_not_nested(self):
        d = {"key1": "Word1 word2", "key2": "word2 word3"}
        required_keys = {'key1', 'key2'}

        expected = [
            ('key1', 'Word1 word2'),
            ('key2', 'word2 word3'),
        ]
        self.assertEqual(expected, find_suitable_keys(d, required_keys))

        expected = [
            ('key1', 'Word1 word2'),
        ]
        required_keys = {'key1', 'KEY2'}
        self.assertEqual(expected, find_suitable_keys(d, required_keys))

    def test_nested(self):
        d = {
            "key1": "val1",
            "key2": {
                "subkey1": "subval1",
                "subkey2": "subval2"
            },
            "key3": "val3"
        }
        required_keys = {"key1", "key2"}
        expected = [
            ('key1', 'val1'),
            ('subkey1', 'subval1'),
            ('subkey2', 'subval2'),
        ]
        self.assertEqual(find_suitable_keys(d, required_keys), expected)

        required_keys = {"KEY1", "key2"}
        expected = [
            ('subkey1', 'subval1'),
            ('subkey2', 'subval2'),
        ]
        self.assertEqual(find_suitable_keys(d, required_keys), expected)

        required_keys = {"key3", "subkey2"}
        expected = [
            ('subkey2', 'subval2'),
            ('key3', 'val3'),
        ]
        self.assertEqual(find_suitable_keys(d, required_keys), expected)


class TestProcessValue(TestCase):
    def test_register(self):
        expected = {('key1', 'word1'), ('key1', 'word2')}
        result = set()
        process_value(key='key1', value='Word1 word2',
                      tokens={"word1", "word2"},
                      callback=lambda key, token: result.add((key, token)))
        self.assertEqual(expected, result)

        expected = {('key1', 'wOrD1'), ('key1', 'WoRd2')}
        result = set()
        process_value(key='key1', value='Word1 word2',
                      tokens={"wOrD1", "WoRd2"},
                      callback=lambda key, token: result.add((key, token)))
        self.assertEqual(expected, result)

    def test_no_tokens(self):
        result = set()
        process_value(key='key1', value='Word1 word2',
                      tokens=set(),
                      callback=lambda key, token: result.add((key, token)))
        self.assertEqual(result, set())

    def test_token_equal_value(self):
        expected = {('key1', 'WoRD1 wOrd2')}
        result = set()
        process_value(key='key1', value='Word1 word2',
                      tokens={"WoRD1 wOrd2"},
                      callback=lambda key, token: result.add((key, token)))
        self.assertEqual(expected, result)

    def test_token_one_symbol(self):
        expected = {('key1', 'w')}
        result = set()
        process_value(key='key1', value='Word1 word2',
                      tokens={"w"},
                      callback=lambda key, token: result.add((key, token)))
        self.assertEqual(expected, result)

    def test_many_tokens_in_value(self):
        expected = UnorderedList((('key1', 'home'),))
        result = UnorderedList()
        process_value(key='key1', value='boom home house home',
                      tokens={"home"},
                      callback=lambda key, token: result.append((key, token)))
        print(expected, result)
        self.assertEqual(expected, result)

        expected = UnorderedList((('key1', 'home'),))
        result = UnorderedList()
        process_value(key='key1', value='boom hOme house home',
                      tokens={"home"},
                      callback=lambda key, token: result.append((key, token)))
        print(expected, result)
        self.assertEqual(expected, result)

    def test_not_string(self):
        result = UnorderedList()
        process_value(key='key1', value={'key2': 'val2'},
                      tokens={"val2"},
                      callback=lambda key, token: result.append((key, token)))
        self.assertEqual(UnorderedList(), result)


class TestPocessJson(TestCase):
    def test_not_nested(self):
        expected = UnorderedList((('key1', 'WORD1'), ('key1', 'word2')))
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        result = UnorderedList()
        process_json(json_str, required_keys, tokens,
                     callback=lambda key, token: result.append((key, token)))
        self.assertEqual(expected, result)

    # def test_nested(self):
    #     d = '''{
    #         "key1": "val1",
    #         "key2": {
    #             "subkey1": "Word1 word2",
    #             "subkey2": [
    #                 "word2",
    #                 "word3"
    #             ],
    #             "subkey3": {
    #                 "subsub": "word1 word3"
    #             }
    #         }
    #     }'''
    #
    #     expected = UnorderedList((
    #         ('key1', 'WORD1'),
    #         ('key1', 'word2')
    #     ))
    #     required_keys = ["key2", "KEY1"]
    #     tokens = ["WORD1", "word2"]
    #     result = UnorderedList()
    #     process_json(json_str, required_keys, tokens,
    #                  callback=lambda key, token: result.append((key, token)))
    #     self.assertEqual(expected, result)
