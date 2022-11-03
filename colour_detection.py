import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # convert colours to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # we now pick a lower and an upper bound to the colours that we want to extract from the image
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Mask returns part of an image that only has the blue pixels existing
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Compare mask and image pixel by pixel and turn all pixels that are not blue to black
    result = cv2.bitwise_and(frame, frame, mask=mask)
   
    cv2.imshow('frame', result)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()