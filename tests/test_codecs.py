# -*- coding: utf-8 -*-

import os
import unittest

from ircconv import codecs

here = os.path.dirname(__file__)


class TestConversion(unittest.TestCase):
    def test_convert(self):
        filename = os.path.join(here, 'data', 'iso-2022-jp.txt')
        with open(filename, 'rb') as f:
            text = codecs.jis_to_utf8(f.read())

        self.assertMultiLineEqual(text, 'ascii ﾊﾝｶｸ\\~\nゼンカク①∪\n')


if __name__ == '__main__':
    unittest.main()
