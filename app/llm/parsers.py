"""LLM 输出解析器（带容错回退）"""
import json
import re
from typing import Optional, List, Dict, Any


class ParseError(Exception):
    """解析错误"""
    pass


def try_parse_json(text: str) -> Optional[dict]:
    """尝试将文本解析为 JSON，支持多种格式"""
    if not text or not text.strip():
        return None

    text = text.strip()

    # 1. 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. 提取 Markdown 代码块
    code_block = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if code_block:
        try:
            return json.loads(code_block.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. 提取最外层 {} 或 []
    brace_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
    if brace_match:
        try:
            return json.loads(brace_match.group(1))
        except json.JSONDecodeError:
            pass

    return None


def try_parse_json_array(text: str) -> Optional[List[Dict]]:
    """尝试解析 JSON 数组"""
    result = try_parse_json(text)
    if isinstance(result, list):
        return result
    return None


def try_parse_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """尝试解析为整数"""
    if value is None:
        return default
    try:
        return int(float(str(value).replace(',', '').replace('¥', '').replace('元', '')))
    except (ValueError, TypeError):
        return default


def try_parse_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """尝试解析为浮点数"""
    if value is None:
        return default
    try:
        return float(str(value).replace(',', '').replace('¥', '').replace('元', ''))
    except (ValueError, TypeError):
        return default


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """安全获取字典值"""
    return data.get(key, default) if isinstance(data, dict) else default


def parse_intent_result(text: str) -> dict:
    """解析意图识别结果"""
    data = try_parse_json(text) or {}
    return {
        "device_type": safe_get(data, "device_type", "unknown"),
        "constraints": safe_get(data, "constraints", {}),
        "need_clarify": safe_get(data, "need_clarify", False),
        "clarify_question": safe_get(data, "clarify_question", ""),
        "clarify_options": safe_get(data, "clarify_options", []),
    }


def parse_search_results(text: str) -> List[Dict]:
    """解析搜索结果"""
    data = try_parse_json_array(text) or []
    return data


def parse_recommendation(text: str) -> dict:
    """解析推荐摘要"""
    data = try_parse_json(text) or {}
    return {
        "summary": safe_get(data, "summary", ""),
        "reasons": safe_get(data, "recommendation_reasons", []),
    }

