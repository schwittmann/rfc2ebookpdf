import unittest
from rfc2pdf import *

class TestRfc2Pdf(unittest.TestCase):

    def test_split(self):
        vectors = [
            (["1\n", "2\n","3\n"] , [["1\n", "2\n","3\n"]]), # no pagebreak
            (["a\n\x0C\n"] , [["a\n\x0C\n"]]), # pagebreak at end
            (["b\n","\x0C\n", "2\n"] , [["b\n" ,"\x0C\n"], ["2\n"]]),
            (["b\n","xx\x0C\n", "2\n"] , [["b\n" ,"xx\x0C\n"], ["2\n"]]),
            (["b\n","xx\x0C\n", "2\x0C\n"] , [["b\n" ,"xx\x0C\n"], ["2\x0C\n"]]),
            (["b\n","xx\x0C\n", "5", "2\x0C\n"] , [["b\n" ,"xx\x0C\n"], ["5", "2\x0C\n"]]),
        ]
        for k, v in vectors:
            self.assertEqual(list(split_at_pagebreak(k)), v)

if __name__ == '__main__':
    unittest.main()