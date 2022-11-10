import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

      # convert colours to HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    # we now pick a lower and an upper bound to the colours that we want to extract from the image
    lower_orange = np.array([0, 60, 60])
    upper_orange = np.array([20, 255, 255])
    # Mask returns part of an image that only has the orange pixels existing
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Compare mask and image pixel by pixel and turn all pixels that are not blue to black
    result = cv2.bitwise_and(imagem, imagem, mask=mask)
    # cv2.imshow('imagem', result)
    
    contornos,_ = findContours(mask, RETR_TREE, CHAIN_APPROX_SIMPLE)
    maior_x = 0
    maior_y = 0
    maior_comp = 0
    maior_altura = 0
    area = 0
    for contorno in contornos:
        x, y, comprimento, altura = boundingRect(contorno)
        if comprimento*altura > area:
            area = comprimento*altura
            maior_x = x
            maior_y = y
            maior_comp = comprimento
            maior_altura = altura
             
        #rectangle(result, pt1=(x,y), pt2=(x + comprimento, y + altura), color=(0,255,0), thickness=3)
    if area > 2000:
        rectangle(imagem, pt1=(maior_x,maior_y), pt2=(maior_x + maior_comp,maior_y + maior_altura), color=(0,255,0), thickness=3)
    cv2.imshow('imagem', imagem)

    if waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()