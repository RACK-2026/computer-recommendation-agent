"""搜索缓存"""
import json
from datetime import datetime, timedelta
from typing import Optional, List


class SearchCache:
    """内存搜索缓存（LRU）"""

    def __init__(self, max_size: int = 20, ttl_minutes: int = 1440):
        self.max_size = max_size
        self.ttl_minutes = ttl_minutes
        self._cache: dict[str, dict] = {}

    def get(self, key: str) -> Optional[list]:
        entry = self._cache.get(key)
        if not entry:
            return None
        if datetime.now() > entry["expires_at"]:
            del self._cache[key]
            return None
        entry["accessed_at"] = datetime.now()
        return entry["data"]

    def set(self, key: str, data: list):
        self._cache[key] = {
            "data": data,
            "expires_at": datetime.now() + timedelta(minutes=self.ttl_minutes),
            "accessed_at": datetime.now(),
        }
        # LRU 淘汰
        if len(self._cache) > self.max_size:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k]["accessed_at"])
            del self._cache[oldest]

    def make_key(self, device_type: str, constraints: dict) -> str:
        """生成缓存键"""
        parts = [device_type]
        usages = constraints.get("usages", [])
        if isinstance(usages, list):
            parts.extend(sorted(usages))
        budget_min = constraints.get("budget_min", 0)
        budget_max = constraints.get("budget_max", 0)
        if budget_min and budget_max:
            parts.append(f"_{int(budget_min)}-{int(budget_max)}")
        brands = constraints.get("brands", [])
        if isinstance(brands, list) and brands:
            parts.extend(sorted(brands))
        return ":".join(parts)

    def clear(self):
        self._cache.clear()


# 全局缓存
search_cache = SearchCache()

