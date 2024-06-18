import unittest
import ast
from vidParser import Parser

class TestVidParser(unittest.TestCase):
    '''
    Tests for the image parser
    must be run from the vid-reader dir to function
    '''

    def setUp(self):
        '''
        test reader on very easy sample
        '''
        self.p = Parser()

    def test_parse_vid(self):
        '''
        test dividing vid up into frames
        '''
        self.p.parse_vid("data/vid1.mp4", "data")

    def test_write_data(self):
        '''
        test writing data to file
        '''
        self.p.create_data_file("data/test.txt")
        test_data = [1, 2, 3, 4, 5, "test"]
        self.p.write_data(test_data, 77)
        self.p.close_data_file()
        f = open("data/test.txt", "r")
        data = f.read()
        data = ast.literal_eval(data)
        #t = [int(n) for n in data[1] if n.isnumeric()]
        #data = [int(data[0]), t]
        f.close()
        data = list(data)
        self.assertEqual(data, [77,[1,2,3,4,5, "test"]])


if __name__ == '__main__':
    unittest.main()
