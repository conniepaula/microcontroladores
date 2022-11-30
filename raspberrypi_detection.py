import cv2
import websockets
import asyncio
import threading
import numpy as np
from pyzbar.pyzbar import decode
from pytesseract import pytesseract

PORT = 8080

cap = cv2.VideoCapture(0)


async def server(websocket, path):
    print("A client has connected. ")
    try:
        async for message in websocket:
            print("Received message: ", message)
            if "velocidade" in message:
                velocidade = message.split(" ")[1]
                print(velocidade)
            if "direcao" in message:
                direcao = message.split(" ")[1]
                print(direcao)
            sendMessage = input("Enter a message to send: ")
            await websocket.send(sendMessage)
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected.")
        print(e)

x = threading.Thread(target=server, args=(1))
x.start()


def text_detection():

    while True:
        ret, frame = cap.read()
        width = int(cap.get(3))
        height = int(cap.get(4))

        cv2.imshow("frame", frame)

        words_in_image_2 = pytesseract.image_to_string(frame)
        print(words_in_image_2)
        if cv2.waitKey(1) == ord('q'):
            break


def colour_detection():
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
        cv2.imshow('imagem', imagem)

        if waitKey(1) & 0xFF == ord("q"):
            break


def qrcode_detection():
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


cap.release()
cv2.destroyAllWindows()

server = websockets.serve(server, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
