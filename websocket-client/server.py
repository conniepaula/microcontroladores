import websockets
import asyncio

PORT = 8080

print("Server listening on port ", str(PORT))


async def echo(websocket, path):
    print("A client has connected.")
    try:
        async for message in websocket:
            print("Received message: ", message)
            sendMessage = input("Enter a message to send: ")
            await websocket.send(sendMessage)
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected.")
        print(e)
server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
