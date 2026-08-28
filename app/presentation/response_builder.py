"""推荐响应组装（纯函数，不依赖 DB 和 LLM）"""
from typing import List
from ..models.product import ScoredProduct, Product


def build_table_data(scored: List[ScoredProduct], score_breakdowns: dict = None) -> list:
    """组装产品表格数据"""
    return [
        {
            "rank": i + 1,
            "name": f"{s.product.brand} {s.product.model_name}",
            "price": f"¥{s.product.price:,.0f}",
            "original_price": f"¥{s.product.original_price:,.0f}" if s.product.original_price else "",
            "rating": s.total_score,
            "match": s.match_reason,
            "pros": s.product.pros[:3] if s.product.pros else [],
            "cons": s.product.cons[:3] if s.product.cons else [],
            "config": _format_config(s.product),
            "source": s.product.source_website or "",
            "score_breakdown": score_breakdowns.get(s.product.id, {}) if score_breakdowns else
                (s.score_breakdown if hasattr(s, 'score_breakdown') else {}),
        }
        for i, s in enumerate(scored)
    ]


def build_followup_hints(device_name: str) -> list:
    """追问引导按钮"""
    return [
        "想详细了解哪一款？告诉我编号",
        "调整预算再搜推荐",
        "换个用途看看其他推荐",
    ]


def build_empty_response(device_name: str) -> dict:
    """无结果时的响应"""
    return {
        "type": "recommendation",
        "summary": "抱歉，当前没有找到匹配的产品。请调整需求试试。",
        "products": [],
        "charts": {},
        "device_type": device_name,
        "followup_hints": ["换个预算试试", "换个用途看看"],
    }


def _format_config(product: Product) -> str:
    s = product.specs
    parts = []
    if s.cpu: parts.append(s.cpu)
    if s.gpu: parts.append(s.gpu)
    if s.ram: parts.append(s.ram)
    if s.storage: parts.append(s.storage)
    return " | ".join(parts)

