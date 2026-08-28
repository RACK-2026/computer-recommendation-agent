"""产品 DB 查询（仅查询，不包含评分逻辑）"""
import json
from typing import List, Optional, Dict
from sqlalchemy import or_
from ..models.product import (
    ProductModel, AggregatedScoreModel, ReviewModel,
    Product, ProductSpecs
)
from ..models import DeviceType, UserGroup
from ..db.engine import SessionLocal


def search_products(
    device_type: DeviceType,
    brands: List[str] = None,
) -> List[Dict]:
    """按设备类型和品牌查询产品，返回原始数据"""
    db = SessionLocal()
    brands = brands or []
    dt_str = device_type.value

    query = db.query(ProductModel).filter(ProductModel.device_type == dt_str)
    if brands:
        brand_filters = [ProductModel.brand.contains(b) for b in brands]
        query = query.filter(or_(*brand_filters))
    products = query.all()

    results = []
    for p in products:
        agg = db.query(AggregatedScoreModel).filter(
            AggregatedScoreModel.product_id == p.id
        ).first()

        common_pros = []; common_cons = []; suitable_for_list = []
        if agg:
            for field, target in [(agg.common_pros_json, common_pros),
                                  (agg.common_cons_json, common_cons)]:
                if field:
                    try: target.extend(json.loads(field))
                    except: pass
            if agg.suitable_for_json:
                try: suitable_for_list = json.loads(agg.suitable_for_json)
                except: pass

        specs = _parse_specs(p.specs_json)

        # 获取评测来源
        reviews = []
        if agg and agg.total_reviews:
            records = db.query(ReviewModel).filter(
                ReviewModel.product_id == p.id
            ).limit(5).all()
            for r in records:
                reviews.append({
                    "source_name": r.source_name or "",
                    "source_type": r.source_type or "",
                    "source_url": r.source_url or "",
                    "summary": (r.summary or "")[:100],
                    "rating": r.rating,
                    "sentiment": r.sentiment or "",
                })

        rating = agg.overall_score if agg and agg.overall_score else (p.rating or 7.0)

        results.append({
            "product": Product(
                id=p.id, brand=p.brand, series=p.series,
                model_name=p.model_name,
                device_type=DeviceType(dt_str),
                price=p.price or 0, original_price=p.original_price,
                specs=specs,
                pros=common_pros[:5], cons=common_cons[:5],
                rating=round(rating, 1),
                suitable_for=[UserGroup(s) for s in suitable_for_list
                              if s in [ug.value for ug in UserGroup]],
                source_website=p.source_website,
            ),
            "agg_score": agg,
            "common_pros": common_pros, "common_cons": common_cons,
            "suitable_for": suitable_for_list,
            "total_reviews": agg.total_reviews if agg else 0,
            "video_reviews": agg.video_reviews if agg else 0,
            "reviews": reviews,
            "dimension_scores": {
                "性能": round(agg.performance_score, 1) if agg and agg.performance_score else 7.0,
                "散热": round(agg.thermal_score, 1) if agg and agg.thermal_score else 7.0,
                "屏幕": round(agg.display_score, 1) if agg and agg.display_score else 7.0,
                "续航": round(agg.battery_score, 1) if agg and agg.battery_score else 7.0,
                "做工": round(agg.build_score, 1) if agg and agg.build_score else 7.0,
            } if agg else {"性能": 7.0, "散热": 7.0, "屏幕": 7.0, "续航": 7.0, "做工": 7.0}
        })

    try: db.close()
    except: pass
    return results


def has_review_data() -> bool:
    """检查评测数据是否存在"""
    db = SessionLocal()
    try:
        return db.query(AggregatedScoreModel).count() > 0
    finally:
        db.close()


def _parse_specs(specs_json: Optional[str]) -> ProductSpecs:
    if not specs_json:
        return ProductSpecs()
    try:
        return ProductSpecs(**json.loads(specs_json))
    except:
        return ProductSpecs()

