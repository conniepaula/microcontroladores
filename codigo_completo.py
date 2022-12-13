from time import sleep
from datetime import datetime, timedelta
from gpiozero import Motor
import RPi.GPIO as GPIO
import websockets
import asyncio
import cv2
import threading
import numpy as np
from pyzbar.pyzbar import decode
from pytesseract import pytesseract

PORT = 8080

cap = cv2.VideoCapture(0)

detect_text = False
detect_qrcode = False
detect_colour = False

r = 3.47  # raio das rodas em centimetros
vMax = 140
vMin = 0

motorEsq = Motor(24, 22)
motorDir = Motor(7, 8)

encDir = 16
GPIO.setup(encDir, GPIO.IN)
contDir = 0
iDir = datetime.now()
GPIO.add_event_detect(encDir, GPIO.RISING)
vDir = 0
porcent_rec_Dir = 0
porcent_cor_Dir = porcent_rec_Dir


def servidor():
    async def echo(websocket, path):
        print("A client has connected.")
        try:
            async for message in websocket:
                print("Received message: " + message)
                if message == "para":
                    defineVel(0, "esq")
                    defineVel(0, "dir")
                    motorDir.stop()
                    motorEsq.stop()
                elif message == "auto":
                    print("Entrei no modo automatico")
                    pass
                elif message == "qrcode":
                    detect_qrcode = True
                elif message == "texto":
                    detect_text = True
                elif message == "cor":
                    detect_color = True
                else:
                    velocidades = message.split(";")  # Será uma lista
                    vel_esq = float(velocidades[0])/100
                    vel_dir = float(velocidades[1])/100
                    # print(vel_esq)
                    # print(vel_dir)
                    defineVel(vel_esq, "esq")
                    defineVel(vel_dir, "dir")
                await websocket.send(message)
        except websockets.exceptions.ConnectionClosed as e:
            print("Client disconnected.")
            print(e)
        # while True:
        #     sleep(1)

    print("Server listening on port ", str(PORT))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(echo, "localhost", PORT)
    loop.run_until_complete(server)
    loop.run_forever()


x = threading.Thread(target=servidor)
x.start()


def ticsDir(encDir):
    global contDir
    fDir = datetime.now()
    if contDir == 10:
        global porcent_rec_Dir, porcent_cor_Dir, vDir, iDir
        deltaDir = (fDir - iDir)
        vDir = ((3.14)/deltaDir.total_seconds())*r
        if porcent_rec_Dir > 0 and porcent_rec_Dir < 1:
            if vDir > (porcent_rec_Dir*vMax):
                porcent_cor_Dir -= 0.01
                motorDir.forward(speed=porcent_cor_Dir)
            elif vDir < (porcent_rec_Dir*vMax):
                porcent_cor_Dir += 0.01
                motorDir.forward(speed=porcent_cor_Dir)
        elif porcent_rec_Dir < 0 and porcent_rec_Dir > -1:
            if vDir > abs(porcent_rec_Dir*vMax):
                porcent_cor_Dir -= 0.01
                motorDir.backward(speed=abs(porcent_cor_Dir))
            elif vDir < (porcent_rec_Dir*vMax):
                porcent_cor_Dir += 0.01
                motorDir.backward(speed=abs(porcent_cor_Dir))
        iDir = datetime.now()
        contDir = 0
    else:
        contDir += 1


encEsq = 12
GPIO.setup(encEsq, GPIO.IN)
contEsq = 0
iEsq = datetime.now()
GPIO.add_event_detect(encEsq, GPIO.RISING)
vEsq = 0
porcent_rec_Esq = 0
porcent_cor_Esq = porcent_rec_Esq


def ticsEsq(encEsq):
    global contEsq
    fEsq = datetime.now()
    if contEsq == 10:
        global porcent_rec_Esq, porcent_cor_Esq, vEsq, iEsq
        deltaEsq = (fEsq - iEsq)
        vEsq = ((3.14)/deltaEsq.total_seconds())*r
        if porcent_rec_Esq > 0 and porcent_rec_Esq < 0.9:
            if vEsq > (porcent_rec_Esq*vMax):
                porcent_cor_Esq -= 0.01
                motorEsq.forward(speed=porcent_cor_Esq)
            elif vEsq < (porcent_rec_Esq*vMax):
                porcent_cor_Esq += 0.01
                motorEsq.forward(speed=porcent_cor_Esq)
        elif porcent_rec_Esq < 0 and porcent_rec_Esq > -1:
            if vEsq > abs(porcent_rec_Esq*vMax):
                porcent_cor_Esq -= 0.01
                motorEsq.backward(speed=abs(porcent_cor_Esq))
            elif vEsq < (porcent_rec_Esq*vMax):
                porcent_cor_Esq += 0.01
                motorEsq.backward(speed=abs(porcent_cor_Esq))
        iEsq = datetime.now()
        contEsq = 0
    else:
        contEsq += 1


def defineVel(porcent, motor):
    if motor == "dir" or motor == "both":
        global porcent_rec_Dir, porcent_cor_Dir
        porcent_rec_Dir = porcent
        porcent_cor_Dir = porcent_rec_Dir
        if porcent >= 0:
            motorDir.forward(porcent_rec_Dir)
        else:
            motorDir.backward(abs(porcent_rec_Dir))

    if motor == "esq" or motor == "both":
        global porcent_rec_Esq, porcent_cor_Esq
        porcent_rec_Esq = porcent
        porcent_cor_Esq = porcent_rec_Esq
        if porcent >= 0:
            motorEsq.forward(porcent_rec_Esq)
        else:
            motorEsq.backward(abs(porcent_rec_Esq))


def text_detection(frame):
    words_in_image_2 = pytesseract.image_to_string(frame)
    result = "Texto: " + words_in_image_2
    return result


def colour_detection(imagem, cap):

    width = int(cap.get(3))
    height = int(cap.get(4))

    # convert colours to HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # we now pick a lower and an upper bound to the colours that we want to extract from the image
    lower_red = np.array([255, 132, 132])
    upper_red = np.array([255, 0, 0])

    lower_blue = np.array([153, 204, 255])
    upper_blue = np.array([0, 0, 255])

    lower_green = np.array([153, 255, 153])
    upper_green = np.array([0, 255, 0])

    # Mask returns part of an image that only has the orange pixels existing
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = red_mask + blue_mask + green_mask
    # Compare mask and image pixel by pixel and turn all pixels that are not blue to black
    result = cv2.bitwise_and(imagem, imagem, mask=mask)
    # cv2.imshow('imagem', result)

    contornos, _ = findContours(mask, RETR_TREE, CHAIN_APPROX_SIMPLE)
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
        rectangle(imagem, pt1=(maior_x, maior_y), pt2=(
            maior_x + maior_comp, maior_y + maior_altura), color=(0, 255, 0), thickness=3)


def qrcode_detection(frame):
    for barcode in decode(frame):
        # should print the data of the barcode (or barcodes in case there are more than one in img)
        data = barcode.data.decode('utf-8')
        print(data)
        result = "QR: " + data
        points = np.array([barcode.polygon], np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(frame, [points], True, (0, 255, 0), 5)
        points2 = barcode.rect
        cv2.putText(frame, data, (points2[0], points2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    cv2.imshow('result', frame)
    return result


GPIO.add_event_callback(encDir, ticsDir)
GPIO.add_event_callback(encEsq, ticsEsq)

iTeste = datetime.now()
fTeste = datetime.now()
deltaTeste = fTeste - iTeste


while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    if detect_colour == True:
        colour_detection(frame, cap)
        detect_colour = False
    if detect_qrcode == True:
        qrcode_detection(frame)
    if detect_text == True:
        text_detection(frame)
        detect_text = False

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
