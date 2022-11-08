import cv2
import numpy as np
from pyzbar.pyzbar import decode
# getting zbar error but terminal says Defaulting to user installation because normal site-packages is not writeable
# Requirement already satisfied: pyzbar in /Users/connie/Library/Python/3.9/lib/python/site-packages (0.1.9)
cap = cv2.VideoCapture(0)
# cv2.imread('qrcode.png')
while True:
    success, image = cap.read()
    for barcode in decode(img):
        # should print the data of the barcode (or barcodes in case there are more than one in img)
        data = barcode.data.decode('utf-8')
        print(data)
        points = np.array([barcode.polygon], np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(image, [points], True, (0, 255, 0), 5)
        points2 = barcode.rect
        cv2.putText(image, data, (points2[0], points2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('result', image)
    cv2.waitKey(1)
