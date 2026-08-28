"""Tavily 搜索实现"""
import asyncio
from typing import List, Optional, Dict
from tavily import TavilyClient, AsyncTavilyClient
from .engine import SearchEngine, SearchResult
from ..config import settings


class TavilySearchEngine(SearchEngine):
    """Tavily Search API 封装"""

    def __init__(self):
        self.api_key = settings.tavily_api_key
        self._client = None
        self._async_client = None

    @property
    def client(self):
        if not self._client:
            self._client = TavilyClient(api_key=self.api_key)
        return self._client

    @property
    def async_client(self):
        if not self._async_client:
            self._async_client = AsyncTavilyClient(api_key=self.api_key)
        return self._async_client

    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        if not self.api_key or self.api_key == "tvly-your-tavily-key-here":
            return []

        try:
            response = await self.async_client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_answer=True,
                include_domains=["www.jd.com", "item.jd.com", "www.bilibili.com",
                                 "www.zhihu.com", "www.smzdm.com", "detail.tmall.com",
                                 "www.ithome.com", "www.notebookcheck.net",
                                 "www.163.com/dy", "tieba.baidu.com"],
            )

            results = []
            for r in response.get("results", []):
                results.append(SearchResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    content=r.get("content", ""),
                    snippet=r.get("content", "")[:200],
                    score=r.get("score", 0.0),
                ))
            return results

        except Exception as e:
            print(f"[Tavily] 搜索失败: {e}")
            return []

    async def search_batch(self, queries: List[str], max_results: int = 3) -> List[SearchResult]:
        if not queries:
            return []

        tasks = [self.search(q, max_results) for q in queries]
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)

        # 合并去重
        seen_urls = set()
        merged = []
        for results in results_lists:
            if isinstance(results, Exception):
                continue
            for r in results:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    merged.append(r)
        return merged


def get_search_engine() -> Optional[SearchEngine]:
    """获取搜索引擎实例"""
    provider = settings.search_api_provider
    if provider == "tavily" and settings.tavily_api_key and settings.tavily_api_key != "tvly-your-tavily-key-here":
        return TavilySearchEngine()
    return None

