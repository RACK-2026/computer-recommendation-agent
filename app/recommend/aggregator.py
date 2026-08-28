"""聚合推荐器（组合原子模块的薄封装，方便单例使用）"""
from typing import List, Optional, Dict

from ..models import DeviceType
from ..models.product import ScoredProduct
from ..recommend.interfaces import RecommenderInterface
from ..db.product_repo import search_products, has_review_data
from ..recommend.scorer import score_and_sort
from ..presentation.score_breakdown import build_score_breakdowns


class AggregatedRecommender(RecommenderInterface):
    """聚合推荐器（薄封装，委托给各原子模块）"""

    def search_products(
        self,
        device_type: DeviceType,
        budget_min: float = 0,
        budget_max: float = 999999,
        usages: List[str] = None,
        brands: List[str] = None,
    ) -> List[Dict]:
        usages = usages or []
        brands = brands or []

        data = search_products(device_type, brands=brands)

        # 筛选出符合预算范围的产品（放宽版，用于初始展示）
        if budget_max < 999999 and data:
            filtered = []
            for item in data:
                p = item["product"]
                if p.price > 0 and (p.price < budget_min - 2000 or p.price > budget_max + 2000):
                    continue
                filtered.append(item)
            return filtered
        return data

    def score_and_sort(
        self,
        products_data: List[Dict],
        budget_min: float,
        budget_max: float,
        usages: List[str],
    ) -> List[ScoredProduct]:
        return score_and_sort(products_data, budget_min, budget_max, usages)

    def has_data(self) -> bool:
        return has_review_data()

    def close(self):
        pass

