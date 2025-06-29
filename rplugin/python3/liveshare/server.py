import threading
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class EventBus:
    def __init__(self):
        self.listeners = {}

    def on(self, event_name: str):
        def decorator(callback):
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)
            return callback

        return decorator

    async def emit(self, event_name: str, *args, **kwargs):
        for callback in self.listeners.get(event_name, []):
            await callback(*args, **kwargs)


event_bus = EventBus()


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
            await event_bus.emit("message_received", user=user, message=data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user} left the chat")


@app.get("/")
async def root():
    try:
        await event_bus.emit("message_received")
    except Exception as e:
        print(f"[ERROR] Emit failed: {e}")
        return {"message": "Failed to emit event", "error": e}
    return {"message": "Hello World"}


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
