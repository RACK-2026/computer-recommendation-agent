"""会话存储（内存 Dict）"""
from typing import Dict, Optional
from datetime import datetime, timedelta
from .conversation import ConversationState


class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, ConversationState] = {}
        self._last_cleanup = datetime.now()

    def get_or_create(self, session_id: str) -> ConversationState:
        # 每 100 次或每 5 分钟清理一次过期会话
        now = datetime.now()
        if len(self._sessions) > 10 and (now - self._last_cleanup).total_seconds() > 300:
            self.clear_expired(max_age_minutes=30)
            self._last_cleanup = now
        if session_id not in self._sessions:
            self._sessions[session_id] = ConversationState(session_id=session_id)
        return self._sessions[session_id]

    def get(self, session_id: str) -> Optional[ConversationState]:
        return self._sessions.get(session_id)

    def delete(self, session_id: str):
        self._sessions.pop(session_id, None)

    def clear_expired(self, max_age_minutes: int = 30):
        """清理超过 max_age_minutes 未活跃的会话"""
        from datetime import datetime, timedelta
        now = datetime.now()
        expired = [
            sid for sid, state in self._sessions.items()
            if (now - state.last_active) > timedelta(minutes=max_age_minutes)
        ]
        for sid in expired:
            del self._sessions[sid]


# 全局单例
session_store = SessionStore()

