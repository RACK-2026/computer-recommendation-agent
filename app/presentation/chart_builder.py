"""图表数据生成 - 独立于核心业务逻辑，只负责组装前端图表 JSON"""
from typing import List
from ..models.product import ScoredProduct


CHART_COLORS = ["#059669", "#10B981", "#34D399", "#6EE7B7", "#A7F3D0"]
RADAR_LABELS = ["性能", "散热", "屏幕", "续航", "做工"]
DIMENSION_KEYS = ["性能", "散热", "屏幕", "续航", "做工"]


def build_price_chart(scored: List[ScoredProduct]) -> dict:
    """价格对比柱状图数据"""
    return {
        "labels": [f"{s.product.brand} {s.product.model_name}" for s in scored],
        "datasets": [{
            "label": "价格 (元)",
            "data": [s.product.price for s in scored],
            "backgroundColor": CHART_COLORS[:len(scored)],
        }]
    }


def build_radar_chart(scored: List[ScoredProduct]) -> dict:
    """综合评分雷达图数据"""
    return {
        "labels": RADAR_LABELS,
        "datasets": [
            {
                "label": f"{s.product.brand} {s.product.model_name}",
                "data": [
                    s.dimension_scores.get(k, 7) for k in DIMENSION_KEYS
                ]
            }
            for s in scored
        ]
    }

