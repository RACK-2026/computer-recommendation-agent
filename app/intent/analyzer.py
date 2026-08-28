"""LLM 意图分析"""
from typing import Optional, Dict
from ..core.conversation import ConversationState
from ..llm.client import llm_client
from ..llm.prompts import INTENT_SYSTEM_PROMPT, INTENT_USER_TEMPLATE
from ..llm.parsers import parse_intent_result
from .fallback import keyword_fallback


async def analyze_with_llm(content: str, state: ConversationState) -> dict:
    """用 LLM 分析用户意图，失败时降级到关键词匹配"""
    recent = state.message_history[-6:-1] if len(state.message_history) > 1 else []
    history_str = "; ".join(
        f"{m['role']}: {m['content'][:50]}" for m in recent
    ) if recent else "无历史"

    try:
        messages = [
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user", "content": INTENT_USER_TEMPLATE.format(
                user_message=content, history=history_str
            )}
        ]
        raw = await llm_client.extract_json(messages)
        return parse_intent_result(raw)
    except Exception:
        return keyword_fallback(content, state)

