import unittest
import cv2
from reader import Reader

OUT = 'data/out.png'

class TestOCRMethods(unittest.TestCase):
    '''
    Tests for the image parser
    must be run from the vid-reader dir to function
    '''
    def setUp(self):
        '''
        setup called before each test
        '''
        self.r = Reader()

    def test_easy_one(self):
        '''
        test reader on very easy sample
        '''
        #r = Reader()
        img = cv2.imread('data/easy1.png')
        data = self.r.read_image(img, OUT)
        self.assertEqual(len(data), 6)
        line = ""
        for (_, word, _) in data:
            line += word
            line += " "
        line = line[:-1]
        self.assertEqual(line, "This text is easy to extract")

    def test_easy_two(self):
        '''
        test reader on slightly harder sample
        '''
        #r = Reader()
        img = cv2.imread('data/easy2.png')
        data = self.r.read_image(img, OUT)
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
        '''
        test reader on single overview column
        '''
        img = cv2.imread('data/test7.png')
        data = self.r.read_image(img, OUT)
        nums = []
        for (_, num, _) in data:
            nums.append(int(num))
        test_arr = [0, 0, 501, 348, 158, 9, 0, 0, 0, 104, 67,
            557, 0, 0, 42, 184, 363, 471, 108, 0, 269,
            264, 278, 165, 68]
        self.assertEqual(len(nums), len(test_arr))
        self.assertEqual(nums, test_arr)

    def test_collate_rows(self):
        '''
        test creation of row data from simple overview sample
        '''
        img = cv2.imread('data/test2.png')
        data = self.r.read_image(img, OUT, draw_bounding_boxes=True)
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
        '''
        test creation of row data on complex overview sample
        '''
        # TODO: this
        img = cv2.imread('data/test4.png')
        data = self.r.read_image(img, OUT, draw_bounding_boxes=True)
        rows = self.r.collate_data(data)
        for row in rows:
            print(row)

    def test_clean_data(self):
        '''
        test clean data method on example dirty imput
        '''
        data_in = [
            ['Overview (test)'],
            ['General', 'Targets', 'Mining', 'WarpTo', 'AlL', 'test'],
            ['Distance', 'Name', 'Velocity', 'Radial Velocity', 'Transversal Velocity', 'Angular'],
            ['134', 'km', 'Rhea Izalith', 'Sigil', '0.00'],
            ['153 km', 'Ignis Firefang', 'Magnate', '0.00'],
            ['3,790', 'Tyranikus Rex', 'Caracal', '3', '3', '0.05'],
            ['127', 'km', 'GefestRUS', 'Vexor', '23,084', '6,139', '23,001', '10.35'],
            ['3,060 k', 'Seriy Kot', 'Caracal', 'Is', '262', '262', '9', '0.00'],
            ['152', 'km', 'Zarkhon', 'Scorpion', '0', '0.00'],
            ['148 km', 'DJ TheDoctorUK', 'Praxis', '0', '0.00'],
            ['150 km', 'Kenneth McArthur', 'Badger', '0.00'],
            ['143 km', 'fm112', 'Tayra', '89', '-62', '63', '0.03'],
            ['130 km', 'Emady White', 'Hoarder', '368', '195', '296', '0.13'],
            ['143 km', 'R2314', 'Capsule', '180', '-125', '128', '0.05'],
            ['174', 'km', 'breaker', 'Capsule', '0', '0.00'],
            ['507,542', 'Ghostrev', 'Minmatar Shuttl', '336,52', '2,425,825,792', '595,895', '0.07'],
            ['138 km', 'Gaowan Dragonson', 'Council Diploma', '655', '355', '546', '0.23'],
            ['138 km', 'Ibis', 'Ibis', '0.00'],
            ['129', 'km', 'Por Prees', 'Velator', '0.00'],
            ['187', 'km', 'Lenil', 'Bustard', '67,723', '58,237', '37,867', '11.55'],
            ['353 km', 'Lucky', '9', 'Bustard', '125', '117', '43', '0.01'],
            ['5,242', 'erie coincidence', 'Occator', '139', '-122', '69', '0.76'],
            ['147', 'km', 'TheLordGoth', 'Thrasher', '303', '-218', '212', '0.08'],
            ['133 km', 'Chtulu Incarnate', 'Coercer', 'Is', '334', '167', '289', '0.12'],
            ['114', 'km', 'Takaya Nono', 'Buzzard', '0.00'],
            ['145 km', 'Clark Sven', 'Tengu', '7,576', '-5,633', '5,414', '2.14'],
            ['Type'],
            ['Navy'],
            ['Zorg'],
            ['Navy'],
        ]
        expected_out_zeros = [
            [134, 'Rhea Izalith', 'Sigil', 0, 0, 0, 0.0],
            [153, 'Ignis Firefang', 'Magnate', 0, 0, 0, 0.0],
            [3790, 'Tyranikus Rex', 'Caracal', 3, 3, 0, 0.05],
            [127, 'GefestRUS', 'Vexor', 23084, 6139, 23001, 10.35],
            [3060, 'Seriy Kot', 'Caracal', 'Is', 262, 262, 9, 0.0],
            [152, 'Zarkhon', 'Scorpion', 0, 0, 0, 0.0],
            [148, 'DJ TheDoctorUK', 'Praxis', 0, 0, 0, 0.0],
            [150, 'Kenneth McArthur', 'Badger', 0, 0, 0, 0.0],
            [143, 'fm112', 'Tayra', 89, -62, 63, 0.03],
            [130, 'Emady White', 'Hoarder', 368, 195, 296, 0.13],
            [143, 'R2314', 'Capsule', 180, -125, 128, 0.05],
            [174, 'breaker', 'Capsule', 0, 0, 0, 0.0],
            [507542, 'Ghostrev', 'Minmatar Shuttl', 33652, 2425825792, 595895, 0.07],
            [138, 'Gaowan Dragonson', 'Council Diploma', 655, 355, 546, 0.23],
            [138, 'Ibis', 'Ibis', 0, 0, 0, 0.0],
            [129, 'Por Prees', 'Velator', 0, 0, 0, 0.0],
            [187, 'Lenil', 'Bustard', 67723, 58237, 37867, 11.55],
            [353, 'Lucky', 9, 'Bustard', 125, 117, 43, 0.01],
            [5242, 'erie coincidence', 'Occator', 139, -122, 69, 0.76],
            [147, 'TheLordGoth', 'Thrasher', 303, -218, 212, 0.08],
            [133, 'Chtulu Incarnate', 'Coercer', 'Is', 334, 167, 289, 0.12],
            [114, 'Takaya Nono', 'Buzzard', 0, 0, 0, 0.0],
            [145, 'Clark Sven', 'Tengu', 7576, -5633, 5414, 2.14],
        ]
        out = self.r.cleanup_data(data_in)
        self.assertEqual(out, expected_out_zeros)

if __name__ == '__main__':
    unittest.main()
