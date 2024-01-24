import unittest
from bulk_convert import *

class TestBulk(unittest.TestCase):

    def test_pad_rfc_name(self):
        self.assertEqual(pad_rfc_name("rfc13"), 'rfc0013')
        self.assertEqual(pad_rfc_name("rfc123"), 'rfc0123')
        self.assertEqual(pad_rfc_name("rfc9876"), 'rfc9876')

if __name__ == '__main__':
    unittest.main()