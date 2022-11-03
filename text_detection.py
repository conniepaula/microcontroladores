import cv2
from pytesseract import pytesseract

img = cv2.imread('test.jpg')

words_in_image = pytesseract.image_to_string(img)

print(words_in_image)