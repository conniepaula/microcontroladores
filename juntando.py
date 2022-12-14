import cv2
import websockets
import asyncio
import threading
import numpy as np
from time import sleep
from pyzbar.pyzbar import decode
from pytesseract import pytesseract

PORT = 8080

cap = cv2.VideoCapture(0)

detect_text = False
detect_qrcode = False
detect_colour = False


def servidor():

    async def echo(websocket, path):
        global detect_text
        global detect_qrcode
        global detect_colour
        print("A client has connected. ")
        try:
            async for message in websocket:
                print("Received message: ", message)
                if "detectar texto" in message:
                    detect_text = True
                elif "detectar qrcode" in message:
                    detect_qrcode = True
                elif "detectar cor" in message:
                    detect_colour = True
                # sendMessage = input("Enter a message to send: ")
                # await websocket.send(sendMessage)
        except websockets.exceptions.ConnectionClosed as e:
            print("Client disconnected.")
            print(e)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(echo, "localhost", PORT)
    loop.run_until_complete(server)
    loop.run_forever()

    # while True:
    #     sleep(1)


x = threading.Thread(target=servidor)
x.start()


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
