import cv2
import numpy as np
import imutils
import easyocr

DEBUG = False

PATH = "data/"
OUT = PATH+"out.png"
EASY = PATH + "easy1.png"
EASY_TWO = PATH + "easy2.png"
EASY_TEST = PATH + "test4.png"

TES_CONFIG = '--psm 6 --tessdata-dir "pyTesTrainData"'
TES_LANG = 'eng_slashed_zeros'

ROW_HIGHT_TOLLERANCE_PX = 50

class Reader():
    # Preprocessing funcs
    def grayscale(self, img):
        '''
        convert image to grayscale
        '''
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def denoise(img):
        '''
        slightly blure image to reduce noise
        '''
        return cv2.medianBlur(img, 5)

    def sharpen(self, img):
        '''
        sharpen image via Laplacian filter
        '''
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        return cv2.filter2D(img, -1, kernel)

    def adaptive_binarization(self, img):
        '''
        use addaptive thresholding to binarize img
        '''
        thresh = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    def otsu_binarization(self, img):
        '''
        threshold the image using Otsu's thresholding method
        '''
        return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    def dist_thresh(self, img):
        '''
        apply distance transformation, normalice, then thresh
        '''
        img = cv2.distanceTransform(img, cv2.DIST_L2, 5)
        img = cv2.normalize(img, img, 0, 1.0, cv2.NORM_MINMAX)
        img = (img * 255).astype("uint8")

        img = cv2.threshold(img, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return img

    def resize(self, img, scale):
        '''
        resize image to make reading easier
        '''
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)


    # can also try dilation, erosion, and canny edge detection

    def preprocessing(self, img):
        '''
        preprocessing steps for image
        '''
        img = self.grayscale(img)
        if img.shape[1] < 2000:
            # only resize and blur if img is too small
            img = imutils.resize(img, width=2000)
            img = cv2.blur(img,(5,5)) # slight blur, no idea why this works
        #img = otsu_binarization(img) # significantly worsens preformance
        return img


    def draw_bounding_boxes(self, img, img_data, img_out):
        '''
        take image data and draw bounding boxes around all text
        '''
        # draw boxes
        for line in resimg_dataults:
            # if conf level > 0
            if line[2] > 0.0:
                corners = line[0]
                top_left = (int(corners[0][0]), int(corners[0][1]))
                bottom_right = (int(corners[2][0]), int(corners[2][1]))

                # params
                green = (0, 255, 0)
                thicknes = 3
                cv2.rectangle(img, top_left, bottom_right, green, thicknes)
        cv2.imwrite(img_out, img)

    def collate_data(self, data):
        '''
        take indivigual data entries and combime them into overview rows
        '''
        rows = []
        row = []
        rowYPos = -100
        for ent in data:
            # if first entry
            if rowYPos == -100:
                rowYPos = ent[0][0][1]
                row.append(ent[1])
                continue
            y = ent[0][0][1]
            if y < (rowYPos + ROW_HIGHT_TOLLERANCE_PX) and y > (rowYPos - ROW_HIGHT_TOLLERANCE_PX):
                row.append(ent[1])
                continue
            rows.append(row)
            row = [ent[1]]
            rowYPos = y
        rows.append(row)
        return rows


    def read_image(self, img_path, output_path, draw_bounding_boxes=False):
        '''
        take a file path and retun info in image
        '''

        # read image
        img = cv2.imread(img_path)
        img = self.preprocessing(img)
        text_reader = easyocr.Reader(['en'], gpu=True) #Initialzing the ocr
        results = text_reader.readtext(img)

        if draw_bounding_boxes:
            self.draw_bounding_box(img, results, output_path)

        if DEBUG:
            for (coords, text, prob) in results:
                print(str(coords)+" "+str(text)+" "+str(prob))
        return results
