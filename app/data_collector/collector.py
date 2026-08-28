"""评测数据采集器 - 对每款产品搜索多源评测并解析"""
import asyncio
import json
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.product import (
    ProductModel, ReviewModel,
    AggregatedScoreModel
)
from ..db.engine import SessionLocal
from ..search.tavily_engine import get_search_engine
from ..search.engine import SearchResult
from .product_list import get_product_list
from .review_parser import parse_review_content, aggregate_reviews


class ReviewCollector:
    """评测采集器：搜索 → 解析 → 入库"""

    def __init__(self, batch_size: int = 5):
        self.engine = get_search_engine()
        self.batch_size = batch_size

    async def collect_all(self, progress_callback=None) -> Dict:
        """采集所有产品的评测数据"""
        products = get_product_list()
        total = len(products)
        results = {"total": total, "success": 0, "failed": 0, "reviews_collected": 0}

        for i, prod in enumerate(products):
            try:
                if progress_callback:
                    progress_callback(i + 1, total, prod["model"])

                count = await self.collect_one(prod)
                if count > 0:
                    results["success"] += 1
                    results["reviews_collected"] += count
                else:
                    results["failed"] += 1

            except Exception as e:
                results["failed"] += 1

            # 每批休眠避免API限流
            if (i + 1) % self.batch_size == 0:
                await asyncio.sleep(1)

        return results

    async def collect_one(self, product_info: Dict) -> int:
        """采集单个产品的评测"""
        product_name = product_info["model"]
        device = product_info["device"]

        if not self.engine:
            return 0

        # 搜索多个方向
        queries = [
            f"{product_name} 评测 优缺点",
            f"{product_name} 值得买吗 体验",
            f"{product_name} 测评 2025",
        ]

        all_results = await self.engine.search_batch(queries, max_results=5)
        if not all_results:
            return 0

        # 取前10条结果
        results = all_results[:10]

        # 解析每条结果
        reviews = []
        for r in results:
            parsed = await parse_review_content(
                title=r.title,
                content=f"{r.snippet}\n{r.content[:2000]}" if r.content else r.snippet,
                source_name=self._detect_source(r.url),
                source_url=r.url,
            )
            if parsed:
                # 推断来源类型
                parsed["source_type"] = self._detect_source_type(r.url, r.title)
                reviews.append(parsed)

        if not reviews:
            return 0

        # 存入数据库
        db = SessionLocal()
        try:
            # 查找或创建产品
            product = db.query(ProductModel).filter(
                ProductModel.model_name.ilike(f"%{product_name}%")
            ).first()

            if not product:
                product = ProductModel(
                    brand=product_info["brand"],
                    series=product_info.get("series", ""),
                    model_name=product_name,
                    device_type="笔记本" if device == "laptop" else "台式机",
                    price=0,
                )
                db.add(product)
                db.flush()

            # 删除旧的评测
            db.query(ReviewModel).filter(ReviewModel.product_id == product.id).delete()

            # 插入新评测
            for r in reviews:
                review = ReviewModel(
                    product_id=product.id,
                    source_type=r.get("source_type", "article"),
                    source_name=r.get("source_name", ""),
                    source_url=r.get("source_url", ""),
                    title="",
                    summary=r.get("summary", ""),
                    pros_json=json.dumps(r.get("pros", []), ensure_ascii=False),
                    cons_json=json.dumps(r.get("cons", []), ensure_ascii=False),
                    rating=r.get("rating"),
                    sentiment=r.get("sentiment", "neutral"),
                )
                db.add(review)

            # 聚合评分
            agg_data = await aggregate_reviews(reviews)
            if agg_data:
                # 删除旧聚合
                db.query(AggregatedScoreModel).filter(
                    AggregatedScoreModel.product_id == product.id
                ).delete()

                agg = AggregatedScoreModel(
                    product_id=product.id,
                    overall_score=agg_data.get("overall_score"),
                    positive_rate=agg_data.get("positive_rate"),
                    performance_score=agg_data.get("performance_score"),
                    thermal_score=agg_data.get("thermal_score"),
                    display_score=agg_data.get("display_score"),
                    battery_score=agg_data.get("battery_score"),
                    build_score=agg_data.get("build_score"),
                    price_score=agg_data.get("price_score"),
                    total_reviews=len(reviews),
                    video_reviews=sum(1 for r in reviews if r.get("source_type") == "video"),
                    article_reviews=sum(1 for r in reviews if r.get("source_type") == "article"),
                    common_pros_json=json.dumps(agg_data.get("common_pros", []), ensure_ascii=False),
                    common_cons_json=json.dumps(agg_data.get("common_cons", []), ensure_ascii=False),
                    suitable_for_json=json.dumps(agg_data.get("suitable_for", []), ensure_ascii=False),
                )
                db.add(agg)

            db.commit()
            return len(reviews)

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _detect_source(self, url: str) -> str:
        """从URL识别来源平台"""
        url_lower = url.lower()
        if "bilibili" in url_lower or "b23" in url_lower:
            return "B站"
        elif "zhihu" in url_lower:
            return "知乎"
        elif "smzdm" in url_lower:
            return "什么值得买"
        elif "jd.com" in url_lower:
            return "京东"
        elif "taobao" in url_lower or "tmall" in url_lower:
            return "淘宝"
        elif "youtube" in url_lower or "youtu.be" in url_lower:
            return "YouTube"
        elif "chiphell" in url_lower or "chh" in url_lower:
            return "Chiphell"
        elif "douyin" in url_lower or "iesdouyin" in url_lower:
            return "抖音"
        elif "163.com" in url_lower or "netease" in url_lower:
            return "网易"
        elif "ithome" in url_lower:
            return "IT之家"
        elif "pcpop" in url_lower:
            return "泡泡网"
        elif "zealer" in url_lower:
            return "Zealer"
        elif "sohu" in url_lower or "sina" in url_lower:
            return "门户网站"
        elif "tieba" in url_lower or "baidu" in url_lower:
            return "贴吧"
        return "网络"

    def _detect_source_type(self, url: str, title: str) -> str:
        """推断评测类型"""
        url_lower = url.lower()
        title_lower = title.lower()

        # 视频
        if any(k in url_lower for k in ["bilibili", "b23", "youtube", "douyin", "ixigua"]):
            return "video"
        if any(k in title_lower for k in ["视频", "vlog", "评测", "测评", "开箱"]):
            # 可能也是视频，但保守处理
            if any(k in url_lower for k in ["bilibili", "youtube"]):
                return "video"

        # 电商
        if any(k in url_lower for k in ["jd.com", "taobao", "tmall", "suning"]):
            return "ecommerce"

        # 论坛
        if any(k in url_lower for k in ["tieba", "chiphell", "v2ex", "nga"]):
            return "forum"

        # 默认当作文章
        return "article"

