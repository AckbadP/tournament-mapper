import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import argparse
import imutils

PATH = "data/"
OUT = PATH+"out.png"
EASY = PATH + "easy1.png"
EASY_TWO = PATH + "easy2.png"
EASY_TEST = PATH + "test6.png"

# ref: https://www.datacamp.com/tutorial/optical-character-recognition-ocr-in-python-with-pytesseract
def image_to_text(input_img):
    '''
    A func to read text from inages
    '''

    img = cv2.imread(input_img)
    text = pytesseract.image_to_string(img)

    return text.strip()

def image_to_data(input_img):
    '''
    A func to read data from images
    '''

    img = cv2.imread(input_img)
    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    return data

def draw_bounding_boxes(img_in, img_out):
    img = cv2.imread(img_in)
    img = preprocessing(img)
    text = pytesseract.image_to_string(img)
    print(text.strip())

   # Extract data
    data = data = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(data["text"])

    for i in range(n_boxes):
        if data["conf"][i] == -1:
            continue
        # Coordinates
        x, y = data["left"][i], data["top"][i]
        w, h = data["width"][i], data["height"][i]

       # Corners
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        # Box params
        green = (0, 255, 0)
        thickness = 3  # The function-version uses thinner lines

        cv2.rectangle(img, top_left, bottom_right, green, thickness)

    # Save the image with boxes
    cv2.imwrite(img_out, img)


# Preprocessing funcs

def grayscale(img):
    '''
    convert image to grayscale
    '''
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise(img):
    '''
    slightly blure image to reduce noise
    '''
    return cv2.medianBlur(img, 5)

def sharpen(img):
    '''
    sharpen image via Laplacian filter
    '''
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    return cv2.filter2D(img, -1, kernel)

def adaptive_binarization(img):
    '''
    use addaptive thresholding to binarize img
    '''
    thresh = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def otsu_binarization(img):
    '''
    threshold the image using Otsu's thresholding method
    '''
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

def dist_thresh(img):
    '''
    apply distance transformation, normalice, then thresh
    '''
    img = cv2.distanceTransform(img, cv2.DIST_L2, 5)
    img = cv2.normalize(img, img, 0, 1.0, cv2.NORM_MINMAX)
    img = (img * 255).astype("uint8")

    img = cv2.threshold(img, 0, 255,
	    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return img

# can also try dilation, erosion, and canny edge detection

def preprocessing(img):
    img = grayscale(img)
    img = otsu_binarization(img)
    #img = adaptive_binarization(img)
    #img = dist_thresh(img)
    #img = denoise(img)
    #img = sharpen(img)

    return img


print("------ Easy 1 ------")
print(image_to_text(EASY))
print(len(image_to_data(EASY)["text"]))
print("------ Easy 2 ------")
print(image_to_text(EASY_TWO))
print(len(image_to_data(EASY_TWO)["text"]))

print("------ Easy Test ------")
draw_bounding_boxes(EASY_TEST, OUT)
