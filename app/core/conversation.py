"""会话状态和上下文"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..models import DeviceType, ConversationStep
from ..models.product import Product, ScoredProduct


@dataclass
class ConversationState:
    session_id: str
    step: ConversationStep = ConversationStep.GREETING
    device_type: Optional[DeviceType] = None
    constraints: Dict[str, Any] = field(default_factory=dict)
    search_results: Optional[List[Product]] = None
    recommended: Optional[List[ScoredProduct]] = None
    message_history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

    def add_message(self, role: str, content: str):
        self.message_history.append({"role": role, "content": content, "time": datetime.now().isoformat()})
        if len(self.message_history) > 20:
            self.message_history = self.message_history[-20:]
        self.last_active = datetime.now()

