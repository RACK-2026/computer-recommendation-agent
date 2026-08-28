"""搜索查询生成"""
from typing import List
from ..models import DeviceType


def build_queries(device_type: DeviceType, constraints: dict) -> List[str]:
    """根据用户需求生成搜索查询"""
    queries = []
    usages = constraints.get("usages", [])
    budget_min = constraints.get("budget_min") or 0
    budget_max = constraints.get("budget_max") or 0
    brands = constraints.get("brands", [])
    notes = constraints.get("special_notes", "")

    device_keyword = "笔记本电脑" if device_type == DeviceType.LAPTOP else "台式机"

    # 1. 通用搜索
    usage_str = "/".join(usages[:2]) if isinstance(usages, list) and usages else "推荐"
    budget_str = ""
    if budget_min > 0 and budget_max > 0:
        budget_str = f"{int(budget_min)}-{int(budget_max)}元"
    elif budget_min > 0:
        budget_str = f"{int(budget_min)}元"

    base_query = f"{budget_str} {device_keyword} {usage_str} 推荐 2025"
    queries.append(base_query.strip())

    # 2. 评测搜索
    review_query = f"{device_keyword} {usage_str} 评测 优缺点"
    queries.append(review_query.strip())

    # 3. 价格搜索
    if budget_str:
        price_query = f"{budget_str} {device_keyword} 价格 排行"
        queries.append(price_query.strip())

    # 4. 品牌定向
    if isinstance(brands, list) and len(brands) > 0:
        brand_str = " ".join(brands[:2])
        brand_query = f"{brand_str} {device_keyword} {usage_str} 价格"
        queries.append(brand_query.strip())

    # 5. 特殊需求
    if notes and isinstance(notes, str) and len(notes) > 2:
        special_query = f"{device_keyword} {notes} 推荐"
        queries.append(special_query.strip())

    return queries

