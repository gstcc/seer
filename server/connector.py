""" """

import asyncio
import websockets


async def join_session(name: str, host: str, port: int):
    try:
        websocket = await websockets.connect(f"ws://{host}:{port}")
        return websocket
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
