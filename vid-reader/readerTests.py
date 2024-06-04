import unittest
from reader import Reader

OUT = 'data/out.png'

class TestOCRMethods(unittest.TestCase):
    def setUp(self):
        self.r = Reader()

    def test_easy_one(self):
        #r = Reader()
        data = self.r.read_image('data/easy1.png', OUT)
        self.assertEqual(len(data), 6)
        line = ""
        for (_, word, _) in data:
            line += word
            line += " "
        line = line[:-1]
        self.assertEqual(line, "This text is easy to extract")

    def test_easy_two(self):
        #r = Reader()
        data = self.r.read_image('data/easy2.png', OUT)
        line = ""
        for (_, word, _) in data:
            line += word
            line += " "
        line = line.split()
        print(line)
        # image includes 2 > that may or may not be read, this is fine
        self.assertGreater(len(line), 53)
        self.assertLess(len(line), 57)

    def test_signle_column(self):
        data = self.r.read_image('data/test7.png', OUT)
        nums = []
        for (_, num, _) in data:
            nums.append(int(num))
        test_arr = [0, 0, 501, 348, 158, 9, 0, 0, 0, 104, 67,
            557, 0, 0, 42, 184, 363, 471, 108, 0, 269,
            264, 278, 165, 68]
        self.assertEqual(len(nums), len(test_arr))
        self.assertEqual(nums, test_arr)


if __name__ == '__main__':
    unittest.main()