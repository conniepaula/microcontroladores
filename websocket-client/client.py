import websockets
import asyncio

PORT = 8080


async def listen():
    url = "ws://localhost:" + str(PORT)
    async with websockets.connect(url) as ws:
        await ws.send("Hello Server")
        while True:
            message = await ws.recv()
            print(message)

asyncio.get_event_loop().run_until_complete(listen())
