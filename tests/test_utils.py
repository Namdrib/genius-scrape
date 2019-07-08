# -*- coding: utf-8 -*-

import unittest
from genius_scrape import utils


class TestUtils(unittest.TestCase):

    def test_convert_quote_types(self):
        self.assertEqual(utils.convert_quote_types("‘Single’"), "'Single'")
        self.assertEqual(utils.convert_quote_types("“”‘’"), "\"\"\'\'")
        self.assertEqual(utils.convert_quote_types('“Smart”'), '"Smart"')

        self.assertEqual(utils.convert_quote_types("I'm"), "I'm")
        self.assertEqual(utils.convert_quote_types("regular"), "regular")
        self.assertEqual(utils.convert_quote_types(""), "")


if __name__ == '__main__':
    unittest.main()
