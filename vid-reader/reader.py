'''
This is a script to take an input eve image and get the following info
 - the distance of the ship
 - the ship's type
 - the ship's piot
 - the direction of the ship relative to the camera
'''
from PIL import Image
import pytesseract
import cv2
import numpy as np

# ref: https://nanonets.com/blog/ocr-with-tesseract/
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

# pring text in image
def image_text(image):
    print(pytesseract.image_to_string(image).strip())

path = 'data/'
test_image = path + 'test1.png'
img = cv2.imread(test_image)
#print(pytesseract.image_to_string(Image.open('data/test1.png')))
image_text(img)
print("\n--- Grayscale ---\n")
gray_img = get_grayscale(img)
image_text(gray_img)

print("\n--- Thresholding ---\n")
#img = cv2.imread(test_image)
#image_text(thresholding(img))

print("\n--- Opening ---\n")
image_text(opening(img))

print("\n--- Canny-Edge ---\n")
image_text(canny(img))