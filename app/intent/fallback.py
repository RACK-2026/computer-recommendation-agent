"""关键词降级意图分析"""
import re
from typing import Dict
from ..core.conversation import ConversationState


# 品牌名单
BRAND_LIST = ["联想", "华硕", "惠普", "戴尔", "华为", "小米", "苹果", "宏碁",
              "机械革命", "七彩虹", "神舟", "荣耀", "微星", "ROG", "外星人",
              "技嘉", "雷神", "雷蛇", "微软"]


def keyword_fallback(content: str, state: ConversationState) -> dict:
    """关键词匹配降级方案"""
    text = content.lower()
    laptop_kw = ["笔记本", "笔记本电脑", "轻薄本", "游戏本", "laptop"]
    desktop_kw = ["台式机", "台机", "桌面", "desktop", "主机箱"]

    has_laptop = any(k in text for k in laptop_kw)
    has_desktop = any(k in text for k in desktop_kw)

    device_type = "unknown"
    if has_laptop and has_desktop:
        device_type = "both"
    elif has_laptop:
        device_type = "laptop"
    elif has_desktop:
        device_type = "desktop"

    constraints = _extract_budget(text)
    _extract_usages(text, constraints)

    # 品牌
    found = [b for b in BRAND_LIST if b in content]
    if found:
        constraints["brands"] = found

    if device_type == "unknown":
        if state.device_type:
            return {"device_type": state.device_type.value.lower(),
                    "need_clarify": False, "constraints": constraints}
        return {
            "need_clarify": True,
            "clarify_question": "你想了解笔记本还是台式机呢？",
            "clarify_options": ["笔记本", "台式机", "还不知道，都看看"]
        }

    return {"device_type": device_type, "need_clarify": False, "constraints": constraints}


def _extract_budget(text: str) -> dict:
    """从文本中提取预算"""
    constraints = {}
    price_pats = [
        (r'(\d+\.?\d*)[千k]', lambda m: int(float(m.group(1)) * 1000)),
        (r'(\d+\.?\d*)[万w]', lambda m: int(float(m.group(1)) * 10000)),
        (r'(\d+)元', lambda m: int(m.group(1))),
        (r'(\d+)块', lambda m: int(m.group(1))),
    ]
    prices = []
    for pat, fn in price_pats:
        for m in re.finditer(pat, text):
            try:
                prices.append(fn(m))
            except:
                pass
    for m in re.finditer(r'(?<!\d)(\d{4,5})(?!\d)', text):
        try:
            prices.append(int(m.group(1)))
        except:
            pass

    if prices:
        has_cap = any(kw in text for kw in ["以内", "以下", "左右", "不超过", "预算"])
        if has_cap:
            constraints["budget_max"] = max(prices)
        elif len(prices) == 1:
            constraints["budget_max"] = prices[0] * 1.2
        else:
            constraints["budget_min"] = min(prices)
            constraints["budget_max"] = max(prices)
    return constraints


def _extract_usages(text: str, constraints: dict):
    """从文本中提取用途"""
    usage_map = {
        "student": ["学生", "大学", "考研", "学习", "上课", "校园"],
        "gamer": ["游戏", "打游戏", "玩", "3A", "吃鸡", "原神", "steam",
                  "穿越火线", "cf", "逆战", "英雄联盟", "lol", "剑网",
                  "永劫", "瓦罗兰特", "csgo", "cs2", "pubg", "守望"],
        "designer": ["设计", "剪辑", "PS", "PR", "渲染", "建模", "视频", "修图"],
        "office": ["办公", "商务", "出差", "工作", "写文档", "表格"],
        "programmer": ["编程", "写代码", "开发", "程序员", "coding", "程序"],
    }
    usages = []
    for key, kws in usage_map.items():
        if any(k in text for k in kws):
            usages.append(key)
    if usages:
        constraints["usages"] = usages

