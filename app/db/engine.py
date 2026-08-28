"""数据库引擎（独立模块，避免 import 副作用）"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """显式初始化数据库表（在应用启动时调用）"""
    from ..models.product import ProductModel, ReviewModel, AggregatedScoreModel, SearchCacheModel
    Base.metadata.create_all(bind=engine)

