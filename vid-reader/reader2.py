import cv2
import pytesseract
from pytesseract import Output

PATH = "data/"
EASY = PATH + "easy1.png"
EASY_TWO = PATH + "easy2.png"

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

print("------ Easy 1 ------")
print(image_to_text(EASY))
print(len(image_to_data(EASY)["text"]))
print("------ Easy 2 ------")
print(image_to_text(EASY_TWO))
print(len(image_to_data(EASY_TWO)["text"]))
