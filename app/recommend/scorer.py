"""评分算法（纯函数，不依赖 DB）"""
from typing import List, Dict
from ..models.product import ScoredProduct


def score_and_sort(
    products_data: List[Dict],
    budget_min: float,
    budget_max: float,
    usages: List[str],
) -> List[ScoredProduct]:
    """对产品进行评分和排序"""
    scored = []

    for item in products_data:
        p = item["product"]

        # 过滤：排除DIY
        brand = (p.brand or "").lower()
        model = (p.model_name or "").lower()
        if "diy" in brand or "diy" in model:
            continue

        # 过滤：价格超出 ±1000
        if budget_max < 999999 and p.price > 0:
            if p.price < budget_min - 1000 or p.price > budget_max + 1000:
                continue

        dims = item["dimension_scores"]
        agg_rating = p.rating

        # 价格匹配分
        price_score = _calc_price_score(p.price, budget_min, budget_max)

        # 人群匹配分
        match_score, match_reasons = _calc_match_score(
            usages, item.get("suitable_for", [])
        )

        # 评测数加分
        review_bonus = min(0.5, item["total_reviews"] / 20 * 0.5)

        total = agg_rating * 0.5 + price_score * 0.25 + match_score * 0.25 + review_bonus

        scored.append(ScoredProduct(
            product=p,
            total_score=round(total, 1),
            dimension_scores=dims,
            match_reason=match_reasons[0] if match_reasons else "综合推荐"
        ))

    scored.sort(key=lambda x: x.total_score, reverse=True)
    return scored


def _calc_price_score(price: float, budget_min: float, budget_max: float) -> float:
    if price <= 0:
        return 5.0
    if budget_max >= 999999:
        return min(8.0, price / 1000)
    if budget_min <= price <= budget_max:
        return 10.0
    elif price < budget_min:
        return 8.0
    else:
        return max(5.0, 10.0 - (price - budget_max) / 300)


def _calc_match_score(usages: List[str], suitable_for: List[str]) -> tuple:
    score = 7.0
    reasons = []
    ug_map = {"student": "学生", "gamer": "游戏", "office": "办公",
              "designer": "设计", "programmer": "编程"}
    for usage in usages:
        human = ug_map.get(usage, usage)
        for suitable in suitable_for:
            if human in suitable or suitable in human:
                score = min(10, score + 1.5)
                reasons.append(f"适合{human}")
                break
            elif any(k in suitable for k in [human[:2], human.replace("家", "")]):
                score = min(10, score + 0.8)
                reasons.append(f"倾向适合{human}")
                break
    return score, reasons

