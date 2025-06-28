import threading
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user} left the chat")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# --- Server Controller ---
class ServerController:
    def __init__(self, host="127.0.0.1", port=8000):
        self.config = uvicorn.Config(app, host=host, port=port, log_level="info")
        self.server = uvicorn.Server(self.config)
        self.thread = None

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.server.run, daemon=True)
            self.thread.start()
            print(f"Server started on http://{self.config.host}:{self.config.port}")
        else:
            print("Server is already running.")

    def stop(self):
        if self.server and self.thread:
            print("Stopping server...")
            self.server.should_exit = True
            self.thread.join()
            print("Server stopped.")
