import unittest
from reader import Reader

OUT = 'data/out.png'

class TestOCRMethods(unittest.TestCase):
    def test_easy_one(self):
        r = Reader()
        data = r.read_image('data/easy1.png', OUT)
        self.assertEqual(len(data), 6)
        line = ""
        for (_, word, _) in data:
            line += word
            line += " "
        line = line[:-1]
        self.assertEqual(line, "This text is easy to extract")

    def test_easy_two(self):
        r = Reader()
        data = r.read_image('data/easy2.png', OUT)
        line = ""
        for (_, word, _) in data:
            line += word
            line += " "
        line = line.split()
        print(line)
        # image includes 2 > that may or may not be read, this is fine
        self.assertGreater(len(line), 53)
        self.assertLess(len(line), 57)


if __name__ == '__main__':
    unittest.main()