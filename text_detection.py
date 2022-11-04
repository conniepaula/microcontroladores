import cv2
from pytesseract import pytesseract

#img = cv2.imread('test.jpg')

#words_in_image = pytesseract.image_to_string(img)

# checking if code detects text in video

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))


    cv2.imshow("frame", frame)

    words_in_image_2 = pytesseract.image_to_string(frame)
    print(words_in_image_2)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

