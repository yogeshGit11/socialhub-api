from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/activeuser/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from user {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
