from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"web socket User {user_id} connected.")

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        print(f"web socket User {user_id} disconnected.")

    async def send_to_user(self, user_id: int, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)
        else:
            print(f"User {user_id} is not connected. Message not sent.")
