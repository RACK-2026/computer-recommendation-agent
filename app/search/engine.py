"""搜索抽象接口"""
from abc import ABC, abstractmethod
from typing import List, Dict


class SearchResult:
    """搜索结果"""
    def __init__(self, title: str, url: str, content: str, snippet: str = "", score: float = 0.0):
        self.title = title
        self.url = url
        self.content = content
        self.snippet = snippet or content[:200]
        self.score = score

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content[:500],
            "snippet": self.snippet,
            "score": self.score,
        }


class SearchEngine(ABC):
    """搜索引擎抽象基类"""

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """执行搜索"""
        pass

    @abstractmethod
    async def search_batch(self, queries: List[str], max_results: int = 3) -> List[SearchResult]:
        """批量搜索并合并去重"""
        pass

