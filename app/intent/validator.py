"""约束校验 - 检查缺失的必要信息"""
from typing import Optional, Dict
from ..core.conversation import ConversationState


def check_missing_info(state: ConversationState) -> Optional[dict]:
    """检查缺失关键信息，返回需要追问的问题"""
    c = state.constraints
    usages = c.get("usages", [])
    if isinstance(usages, list) and len(usages) == 0:
        return {
            "question": "你的主要用途是什么？我可以更精准推荐 🎯",
            "options": ["学习/学生", "打游戏", "商务办公", "编程/设计"]
        }
    has_budget = "budget_min" in c or "budget_max" in c
    if not has_budget:
        return {
            "question": "你的预算大概在什么范围？💰",
            "options": ["3000-5000元", "5000-7000元", "7000-10000元", "10000元以上"]
        }
    return None


def update_constraints(state: ConversationState, new_constraints: dict):
    """更新约束，不覆盖已有的品牌/用途等非空信息"""
    if not new_constraints or not isinstance(new_constraints, dict):
        return
    for k, v in new_constraints.items():
        existing = state.constraints.get(k)
        if k in ("brands", "usages") and existing and not v:
            continue
        if k == "budget_min" and existing and existing > 0:
            continue
        if k == "budget_max" and existing and existing < 999999:
            continue
        state.constraints[k] = v

