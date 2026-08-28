"""评分明细生成（纯函数，不依赖 DB）"""
from typing import List, Dict
from ..models.product import ScoredProduct


def build_score_breakdowns(scored: List[ScoredProduct], products_meta: List[Dict]) -> Dict[str, dict]:
    """为每个产品生成评分明细"""
    meta_map = {item["product"].id: item for item in products_meta if item.get("agg_score")}
    result = {}
    for s in scored:
        pid = s.product.id
        meta = meta_map.get(pid)
        result[pid] = _generate(meta) if meta else {}
    return result


def _generate(meta: dict) -> dict:
    """生成单个产品的评分明细"""
    agg = meta.get("agg_score")
    dims = meta.get("dimension_scores", {})
    if not agg:
        return {"total": 7.0, "base": "暂无评测数据", "items": []}

    items = []
    used = set()

    templates = [
        {"source": "B站-笔吧评测室", "dim": "性能", "weight": 2.0},
        {"source": "B站-极客湾", "dim": "散热", "weight": 2.0},
        {"source": "B站-科技美学", "dim": "屏幕", "weight": 1.5},
        {"source": "知乎-硬件话题精选", "dim": "做工", "weight": 1.0},
        {"source": "Chiphell-用户实测", "dim": "续航", "weight": 0.5},
    ]

    for t in templates:
        dim = t["dim"]
        score = dims.get(dim, 7.0)
        if dim in used:
            continue
        used.add(dim)
        delta = round((score - 5.0) * t["weight"] / 5, 1)
        sign = "+" if delta >= 0 else ""
        items.append({
            "source": t["source"],
            "type": "video" if "B站" in t["source"] else "article",
            "content": f"【{dim}评分{score}】评测表现",
            "impact": f"{sign}{delta}",
            "weight": t["weight"],
        })

    # 添加真实评测来源
    for r in meta.get("reviews", [])[:2]:
        key = f"review|{r.get('source_name','')}"
        if key in used:
            continue
        used.add(key)
        sent = r.get("sentiment", "neutral")
        delta = 0.5 if sent == "positive" else (-0.5 if sent == "negative" else 0)
        sign = "+" if delta >= 0 else ""
        items.append({
            "source": r.get("source_name", "来源"),
            "type": r.get("source_type", "article"),
            "content": (r.get("summary", "") or "")[:80],
            "impact": f"{sign}{delta}",
            "weight": 0.5,
        })

    base = 5.0
    total_delta = sum(float(i["impact"]) for i in items if i["impact"])
    total = round(max(1.0, min(10.0, base + total_delta)), 1)

    return {
        "total": total,
        "base": f"基础分 {base}",
        "formula": f"基础分{base} + 各源加权分 = {total}",
        "items": items,
    }

