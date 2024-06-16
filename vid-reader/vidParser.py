import cv2
import os

DEBUG = True

class Parser():
    '''
    
    '''

    # ref: https://stackoverflow.com/a/47632941/20586552
    def parse_vid(self, pathIn, pathOut, fps=1):
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
