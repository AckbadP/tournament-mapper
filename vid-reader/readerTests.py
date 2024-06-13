import unittest
from reader import Reader

OUT = 'data/out.png'

class TestOCRMethods(unittest.TestCase):
    '''
    Tests for the image parser
    must be run from the vid-reader dir to function
    '''
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

    def test_collate_rows(self):
        data = self.r.read_image('data/test2.png', OUT, draw_bounding_boxes=True)
        rows = self.r.collate_data(data)
        expected_rows = [
            ['Overview (test', 'Not Saved)'],
            ['General', 'Targets', 'Mining', 'WarpTo', 'All', 'test'],
            ['Distan', 'Name', 'Type', 'Size', 'Velocity', 'Angular'],
            ['19', 'km', 'CONCORD Police Capta', 'CONCORD', 'Police', '300', 'M', '38', '0.10'],
            ['19', 'km', 'CONCORD Police Comm', 'CONCORD Police', '1,200', 'M', '287', '0.76'],
            ['38', 'km', 'CONCORD', 'Police Capta', 'CONCORD', 'Police', '300', 'M', '784', '119']
        ]
        self.assertEqual(len(rows), len(expected_rows))
        self.assertEqual(rows, expected_rows)
        #for row in rows:
        #    print(row)

    def test_collate_rows_complex(self):
        data = self.r.read_image('data/test4.png', OUT, draw_bounding_boxes=True)
        rows = self.r.collate_data(data)
        for row in rows:
            print(row)

if __name__ == '__main__':
    unittest.main()