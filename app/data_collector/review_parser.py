"""LLM 评测内容解析 - 从搜索结果的评测文章中提取结构化评价"""
import json
from typing import List, Optional, Dict
from ..llm.client import llm_client
from ..llm.parsers import try_parse_json_array, try_parse_json

# 系统提示词：评测解析
REVIEW_PARSE_SYSTEM_PROMPT = """你是一个专业的电脑评测分析师。从评测内容中提取关键信息。

请分析以下评测内容，提取结构化数据并输出 JSON 对象：

{
  "summary": "用一句话总结这篇评测的核心观点",
  "pros": ["优点1", "优点2", ...],
  "cons": ["缺点1", "缺点2", ...],
  "rating": 7.5,
  "sentiment": "positive/neutral/negative",
  "suitable_for": ["学生", "游戏玩家", "商务办公", "设计师"],
  "highlights": {
    "performance": "性能表现评价（1-2句话）",
    "thermal": "散热表现评价",
    "display": "屏幕表现评价",
    "battery": "续航表现评价",
    "build": "做工质感评价"
  }
}

要求：
1. rating 是 0-10 的分数，基于评测内容判断，不是电商评分
2. pros/cons 各列出 2-4 条，从评测原文中提取
3. sentiment 判断评测整体态度
4. 如果原文没有涉及某个维度，对应字段设为 null
5. suitable_for 推断适合人群（可多选）
6. 只输出 JSON，不要其他文字"""


async def parse_review_content(
    title: str,
    content: str,
    source_name: str,
    source_url: str,
) -> Optional[Dict]:
    """用 LLM 解析单篇评测内容"""
    if not content or len(content.strip()) < 20:
        return None

    try:
        messages = [
            {"role": "system", "content": REVIEW_PARSE_SYSTEM_PROMPT},
            {"role": "user", "content": f"标题：{title}\n\n评测内容：\n{content[:2500]}"}
        ]
        raw = await llm_client.extract_json(messages)
        data = try_parse_json(raw)
        if not data:
            return None

        return {
            "summary": data.get("summary", ""),
            "pros": data.get("pros", []),
            "cons": data.get("cons", []),
            "rating": data.get("rating"),
            "sentiment": data.get("sentiment", "neutral"),
            "suitable_for": data.get("suitable_for", []),
            "highlights": data.get("highlights", {}),
            "source_name": source_name,
            "source_url": source_url,
        }
    except Exception:
        return None


# 批处理提示词：从搜索结果中批量提取评测
SEARCH_RESULT_PARSE_PROMPT = """你是一个电脑评测分析师。分析以下搜索结果的标题和摘要，判断哪些是有效的产品评测。

对每一条结果，判断：
1. 是否是有效的产品评测（review_score: 0-5，5是高质量评测）
2. 评测类型（video/article/forum/ecommerce）
3. 来源平台名称
4. 一句话摘要

输出 JSON 数组：
[
  {
    "title": "原标题",
    "is_review": true/false,
    "review_score": 4,
    "source_type": "video",
    "source_name": "B站",
    "url": "原文链接",
    "summary": "评测摘要",
    "confidence": 0.9
  }
]"""


async def filter_search_results(results: List[Dict]) -> List[Dict]:
    """从搜索结果中筛选出有效评测"""
    if not results:
        return results

    text = "\n---\n".join(
        f"标题: {r.get('title', '')}\n摘要: {r.get('snippet', '')}\n链接: {r.get('url', '')}"
        for r in results[:15]
    )

    try:
        messages = [
            {"role": "system", "content": SEARCH_RESULT_PARSE_PROMPT},
            {"role": "user", "content": text}
        ]
        raw = await llm_client.extract_json(messages)
        parsed = try_parse_json_array(raw) or []

        valid = [p for p in parsed if p.get("is_review") and p.get("confidence", 0) >= 0.5]
        return valid
    except Exception:
        return results[:5]


# 维度评分汇总提示词
DIMENSION_AGGREGATE_PROMPT = """你是一个数据统计分析师。以下是针对某款电脑产品的多篇评测数据，请汇总分析。

输出 JSON：
{
  "overall_score": 7.8,
  "positive_rate": 0.85,
  "performance_score": 8.0,
  "thermal_score": 7.0,
  "display_score": 8.5,
  "battery_score": 6.5,
  "build_score": 8.0,
  "price_score": 7.0,
  "common_pros": ["综合优点1", "综合优点2", "综合优点3", "综合优点4", "综合优点5"],
  "common_cons": ["综合缺点1", "综合缺点2", "综合缺点3"],
  "suitable_for": ["学生", "游戏玩家"]
}

评分标准：0-10分，基于真实评测数据综合判断
positive_rate: 正面评测占比 0-1
common_pros/cons: 汇总5条最常提到的优缺点
suitable_for: 推断适合人群
"""


async def aggregate_reviews(reviews: List[Dict]) -> Dict:
    """汇总所有评测得到聚合评分"""
    if not reviews:
        return {}

    # 构建汇总文本
    lines = []
    for i, r in enumerate(reviews[:15]):
        lines.append(
            f"[评测{i+1}] 来源:{r.get('source_name','')} 类型:{r.get('source_type','')}\n"
            f"评分:{r.get('rating','N/A')} 态度:{r.get('sentiment','')}\n"
            f"优点:{', '.join(r.get('pros', [])[:3])}\n"
            f"缺点:{', '.join(r.get('cons', [])[:3])}\n"
            f"总结:{r.get('summary','')}"
        )

    text = "\n---\n".join(lines)

    try:
        messages = [
            {"role": "system", "content": DIMENSION_AGGREGATE_PROMPT},
            {"role": "user", "content": f"以下是该产品的 {len(reviews)} 篇评测数据：\n\n{text}"}
        ]
        raw = await llm_client.extract_json(messages)
        return try_parse_json(raw) or {}
    except Exception:
        # LLM失败时简单平均
        ratings = [r.get("rating") for r in reviews if r.get("rating")]
        avg = sum(ratings) / len(ratings) if ratings else 7.0
        return {"overall_score": round(avg, 1), "positive_rate": 0.8}

