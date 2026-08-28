"""WebSocket 聊天端点（支持状态流推送）"""
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..core.chat_manager import ChatManager

router = APIRouter()
chat_manager = ChatManager()


async def send_json(ws: WebSocket, data: dict):
    try:
        await ws.send_text(json.dumps(data, ensure_ascii=False))
    except Exception:
        pass


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    session_id = str(uuid.uuid4())[:8]
    first_message = True

    async def status_callback(text: str):
        """推送状态更新"""
        await send_json(websocket, {"type": "status", "content": text})

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            content = msg.get("content", "").strip()
            client_sid = msg.get("session_id", "")

            if client_sid:
                session_id = client_sid

            if not content:
                continue

            if len(content) > 2000:
                await send_json(websocket, {
                    "type": "error",
                    "content": "消息太长了，请精简到 2000 字以内"
                })
                continue

            if first_message:
                await send_json(websocket, {"type": "connected", "session_id": session_id})
                first_message = False

            # 推送状态
            await status_callback("正在分析需求...")

            # 处理消息（传入状态回调）
            result = await chat_manager.handle_message(session_id, content, status_callback)

            # 发送结果
            await send_json(websocket, result)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            await send_json(websocket, {
                "type": "error",
                "content": "抱歉，服务器内部错误，请稍后重试"
            })
        except Exception:
            pass

