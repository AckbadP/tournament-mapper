import unittest
from reader import Reader

OUT = 'data/out.png'

class TestOCRMethods(unittest.TestCase):
    def test_easy_one(self):
        r = Reader()
        data = r.read_image('data/easy1.png', OUT)
        self.assertEqual(len(data), 6)

if __name__ == '__main__':
    uinttest.main()