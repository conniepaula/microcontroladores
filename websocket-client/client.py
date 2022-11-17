import websockets
import asyncio

PORT = 8080


async def listen():
    url = "ws://localhost:" + str(PORT)
    async with websockets.connect(url) as ws:
        sendMessage = input("Enter a message to send: ")
        await ws.send(sendMessage)
        while True:
            message = await ws.recv()
            print(message)

asyncio.get_event_loop().run_until_complete(listen())
