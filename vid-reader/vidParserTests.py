import unittest
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



if __name__ == '__main__':
    unittest.main()
