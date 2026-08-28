"""数据库操作"""
import json
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session

from ..db.engine import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductRepository:
    @staticmethod
    def save_products(db: Session, products: list) -> int:
        """批量保存产品，返回新增数"""
        count = 0
        for p in products:
            exists = db.query(ProductModel).filter(
                ProductModel.model_name == p.model_name,
                ProductModel.device_type == p.device_type.value
            ).first()
            if exists:
                # 更新价格和评分
                exists.price = p.price
                exists.rating = p.rating
                if p.specs:
                    exists.specs_json = p.specs.model_dump_json()
                if p.pros:
                    exists.pros_json = json.dumps(p.pros)
                if p.cons:
                    exists.cons_json = json.dumps(p.cons)
                if p.suitable_for:
                    exists.suitable_for_json = json.dumps([s.value for s in p.suitable_for])
            else:
                record = ProductModel(
                    brand=p.brand, series=p.series, model_name=p.model_name,
                    device_type=p.device_type.value, price=p.price,
                    original_price=p.original_price,
                    specs_json=p.specs.model_dump_json() if p.specs else "{}",
                    pros_json=json.dumps(p.pros), cons_json=json.dumps(p.cons),
                    rating=p.rating,
                    suitable_for_json=json.dumps([s.value for s in p.suitable_for]),
                    review_summary=p.review_summary, source_url=p.source_url,
                    source_website=p.source_website
                )
                db.add(record)
                count += 1
        db.commit()
        return count

    @staticmethod
    def get_by_device_type(db: Session, device_type: str) -> List[ProductModel]:
        return db.query(ProductModel).filter(
            ProductModel.device_type == device_type
        ).order_by(ProductModel.price).all()


class SearchCacheRepository:
    @staticmethod
    def get(db: Session, cache_key: str) -> Optional[str]:
        record = db.query(SearchCacheModel).filter(
            SearchCacheModel.cache_key == cache_key,
            SearchCacheModel.expires_at > datetime.utcnow()
        ).first()
        return record.results_json if record else None

    @staticmethod
    def set(db: Session, cache_key: str, results_json: str, ttl_hours: int = 24):
        record = db.query(SearchCacheModel).filter(
            SearchCacheModel.cache_key == cache_key
        ).first()
        if record:
            record.results_json = results_json
            record.expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        else:
            record = SearchCacheModel(
                cache_key=cache_key,
                results_json=results_json,
                expires_at=datetime.utcnow() + timedelta(hours=ttl_hours)
            )
            db.add(record)
        db.commit()

