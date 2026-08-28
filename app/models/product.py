"""数据模型"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from . import DeviceType, UserGroup
from ..db.engine import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    brand = Column(String(50), index=True)
    series = Column(String(100))
    model_name = Column(String(200), index=True)
    device_type = Column(String(20), index=True)
    price = Column(Float, index=True)
    original_price = Column(Float, nullable=True)
    specs_json = Column(Text)
    pros_json = Column(Text)       # deprecated, kept for compatibility
    cons_json = Column(Text)       # deprecated
    rating = Column(Float)          # deprecated
    suitable_for_json = Column(Text) # deprecated
    review_summary = Column(Text)   # deprecated
    source_url = Column(String(500))
    source_website = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关联
    reviews = relationship("ReviewModel", back_populates="product", cascade="all, delete-orphan")
    agg_score = relationship("AggregatedScoreModel", back_populates="product", uselist=False, cascade="all, delete-orphan")


class ReviewModel(Base):
    """单个评价/评测源"""
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    source_type = Column(String(20))   # video / article / ecommerce / forum
    source_name = Column(String(50))   # B站 / 知乎 / 京东 / 什么值得买
    source_url = Column(String(500))
    title = Column(String(200))
    summary = Column(Text)             # LLM 提取的评测摘要
    pros_json = Column(Text)           # JSON 优点列表
    cons_json = Column(Text)           # JSON 缺点列表
    rating = Column(Float, nullable=True)  # 来源自带的评分
    sentiment = Column(String(10))     # positive / neutral / negative
    author = Column(String(100))
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    product = relationship("ProductModel", back_populates="reviews")


class AggregatedScoreModel(Base):
    """多源聚合评分"""
    __tablename__ = "product_aggregated_scores"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, index=True)

    # 聚合评分
    overall_score = Column(Float)      # 综合评分 0-10
    positive_rate = Column(Float)      # 好评率 0-1

    # 各维度评分 (0-10)
    performance_score = Column(Float)
    thermal_score = Column(Float)
    display_score = Column(Float)
    battery_score = Column(Float)
    build_score = Column(Float)
    price_score = Column(Float)

    # 统计
    total_reviews = Column(Integer, default=0)
    video_reviews = Column(Integer, default=0)
    article_reviews = Column(Integer, default=0)

    # 综合优缺点 (汇总TOP)
    common_pros_json = Column(Text)     # JSON 数组
    common_cons_json = Column(Text)     # JSON 数组

    # 适合人群 (从评价推断)
    suitable_for_json = Column(Text)    # JSON 数组

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    product = relationship("ProductModel", back_populates="agg_score")


class SearchCacheModel(Base):
    __tablename__ = "search_cache"
    id = Column(Integer, primary_key=True)
    cache_key = Column(String(200), unique=True, index=True)
    results_json = Column(Text)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)


# ---------- Pydantic ----------
class ProductSpecs(BaseModel):
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    screen_size: Optional[str] = None
    screen_resolution: Optional[str] = None
    refresh_rate: Optional[str] = None
    weight: Optional[str] = None
    battery: Optional[str] = None
    os: Optional[str] = None


class Product(BaseModel):
    model_config = {"protected_namespaces": ()}
    id: Optional[int] = None
    brand: str = ""
    series: str = ""
    model_name: str = ""
    device_type: DeviceType = DeviceType.LAPTOP
    price: float = 0.0
    original_price: Optional[float] = None
    specs: ProductSpecs = Field(default_factory=ProductSpecs)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    rating: float = 0.0
    suitable_for: List[UserGroup] = Field(default_factory=list)
    review_summary: Optional[str] = None
    source_url: Optional[str] = None
    source_website: Optional[str] = None
    updated_at: Optional[str] = None


class ScoredProduct(BaseModel):
    product: Product
    total_score: float = 0.0
    dimension_scores: dict = Field(default_factory=dict)
    match_reason: str = ""
    score_breakdown: dict = Field(default_factory=dict)

