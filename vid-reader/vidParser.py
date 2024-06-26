import cv2
import os
import lzma
from reader import Reader

DEBUG = True

DEFAULT_OUTFILE_NAME = "data/out.txt"

class Parser:
    '''
    class that handles converting vid to spaceship data
    '''
    def __init__(self):
        self.outfile_exists = False
        self.outfile = None


    # ref: https://stackoverflow.com/a/47632941/20586552
    def parse_vid(self, pathIn, pathOut, fps=1):
        '''
        test func that splits vid into frames
        '''
        count = 0
        vidcap = cv2.VideoCapture(pathIn)
        success, image = vidcap.read()
        success = True

        pathOut = pathOut+"/frames"
        if not os.path.exists(pathOut):
            os.makedirs(pathOut)

        while True:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000 * 1/fps))
            success, image = vidcap.read()
            if not success:
                break

            cv2.imwrite(pathOut+"/frame%d.jpg" % count, image)
            if DEBUG:
                print("read frame "+str(count))
            count += 1

    def create_data_file(self, outfile):
        '''
        create output file
        '''
        if self.outfile_exists:
            return

        #self.outfile = lzma.LZMAFile(outfile, mode="wb")
        self.outfile = open(outfile, "w")
        self.outfile_exists = True

    def close_data_file(self):
        '''
        close outfile
        '''
        self.outfile.close()
        self.out_file_exists = False

    def write_data(self, data, count):
        '''
        write data to compressed file
        '''
        if not self.outfile_exists:
            self.create_data_file(DEFAULT_OUTFILE_NAME)

        if DEBUG:
            print("---------- Frame: "+str(count)+" ----------")
            for line in data:
                print(str(count)+": "+str(line))
            
        data = [count, data]
        self.outfile.write(",".join(str(item) for item in data))
        self.outfile.write("\n")

    def main(self, path_in, path_out, fps=1):
        '''
        main
        '''
        r = Reader()
        count = 0
        vidcap = cv2.VideoCapture(path_in)
        success, image = vidcap.read()
        success = True

        self.out_file_exists = False
        self.create_data_file(path_out)

        while True:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000 * 1/fps))
            success, image = vidcap.read()
            if not success:
                break

            # parse image
            data = r.read_image(image, path_out)
            rows = r.collate_data(data)
            self.write_data(rows, count)

            if DEBUG:
                print("read frame "+str(count))
            count += 1
        self.close_data_file()


if __name__ == '__main__':
    p = Parser()
    #p.main()
