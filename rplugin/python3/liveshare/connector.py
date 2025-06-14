import asyncio
import websockets
import json


class Connector:
    def __init__(self, user: str, host: str, port: int):
        self.user = user
        self.host = host
        self.port = port
        self.websocket = None
        self.listen_task = None

    async def join_session(self):
        try:
            self.websocket = await websockets.connect(
                f"ws://{self.host}:{self.port}/ws/{self.user}"
            )
            print(f"Connected to session as {self.user}")

            # Start the message listener
            self.listen_task = asyncio.create_task(self.listen())
        except Exception as e:
            print(f"Connection failed: {e}")

    async def listen(self):
        try:
            if not self.websocket:
                return
            async for message in self.websocket:
                await self.on_message(message)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")
        except Exception as e:
            print(f"Error in listener: {e}")

    async def send(self, data):
        if self.websocket:
            await self.websocket.send(json.dumps(data))

    async def on_message(self, message):
        pass
