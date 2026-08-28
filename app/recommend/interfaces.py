"""推荐引擎和LLM的抽象接口"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from ..models import DeviceType
from ..models.product import ScoredProduct


class RecommenderInterface(ABC):
    """推荐引擎抽象接口"""

    @abstractmethod
    def search_products(
        self,
        device_type: DeviceType,
        budget_min: float = 0,
        budget_max: float = 999999,
        usages: List[str] = None,
        brands: List[str] = None,
    ) -> List[Dict]:
        ...

    @abstractmethod
    def score_and_sort(
        self,
        products_data: List[Dict],
        budget_min: float,
        budget_max: float,
        usages: List[str],
    ) -> List[ScoredProduct]:
        ...

    @abstractmethod
    def has_data(self) -> bool:
        ...

    @abstractmethod
    def close(self):
        ...


class LLMInterface(ABC):
    """LLM 客户端抽象接口"""

    @abstractmethod
    async def chat(self, messages: List[Dict], **kwargs) -> str:
        ...

    @abstractmethod
    async def extract_json(self, messages: List[Dict], **kwargs) -> str:
        ...

