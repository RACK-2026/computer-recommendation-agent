"""对话编排器（仅做流程控制，不包含具体业务逻辑）"""
from typing import Optional, List

from ..models import DeviceType, ConversationStep
from ..models.product import ScoredProduct
from ..core.conversation import ConversationState
from ..core.session_store import session_store
from ..recommend.aggregator import AggregatedRecommender
from ..recommend.interfaces import RecommenderInterface
from ..intent.analyzer import analyze_with_llm
from ..intent.validator import check_missing_info, update_constraints
from ..presentation.chart_builder import build_price_chart, build_radar_chart
from ..presentation.response_builder import build_table_data, build_followup_hints, build_empty_response
from ..presentation.score_breakdown import build_score_breakdowns


class ChatManager:
    """对话状态机编排器"""

    def __init__(self, recommender: RecommenderInterface = None):
        self.session_store = session_store
        self.recommender = recommender or AggregatedRecommender()

    async def handle_message(self, session_id: str, content: str, status_callback=None) -> dict:
        state = self.session_store.get_or_create(session_id)
        state.add_message("user", content)

        if status_callback:
            await status_callback("正在分析你的需求...")

        # 1. 意图分析
        intent = await analyze_with_llm(content, state)
        if intent.get("need_clarify", False):
            state.step = ConversationStep.CLARIFYING
            return {
                "type": "clarify",
                "content": intent.get("clarify_question", ""),
                "options": intent.get("clarify_options", [])
            }

        # 2. 更新状态
        dt = intent.get("device_type", "unknown")
        device_map = {"laptop": DeviceType.LAPTOP, "desktop": DeviceType.DESKTOP, "both": DeviceType.BOTH}
        if dt in device_map:
            state.device_type = device_map[dt]
        update_constraints(state, intent.get("constraints", {}))

        # 3. 检查缺失信息
        if missing := check_missing_info(state):
            state.step = ConversationStep.CLARIFYING
            return {"type": "clarify", "content": missing["question"], "options": missing.get("options", [])}

        # 4. 查询 + 评分
        if status_callback:
            await status_callback("正在从评测数据库匹配产品...")
        scored = self._query_and_score(state)
        state.recommended = scored

        # 5. 组装响应
        if status_callback:
            await status_callback("正在生成推荐方案...")
        result = self._build_response(scored, state)
        state.add_message("assistant", result.get("summary", ""))
        return result

    def _query_and_score(self, state: ConversationState) -> List[ScoredProduct]:
        """查询+评分（含精确查询和放宽重试）"""
        from ..db.product_repo import search_products
        from ..recommend.scorer import score_and_sort

        device = state.device_type or DeviceType.BOTH
        usages = state.constraints.get("usages", [])
        budget_min = state.constraints.get("budget_min") or 0
        budget_max = state.constraints.get("budget_max") or 999999
        brands = state.constraints.get("brands", [])

        # 精确查询
        data = search_products(device, brands=brands)
        scored = score_and_sort(data, budget_min, budget_max, usages)
        if scored:
            return scored[:5]

        # 放宽预算重试
        if budget_max < 999999:
            relaxed_min = max(0, budget_min - 5000)
            relaxed_max = budget_max + 5000
            data = search_products(device, brands=brands)
            scored = score_and_sort(data, relaxed_min, relaxed_max, usages)
            if scored:
                return scored[:5]
        return []

    def _build_response(self, scored: List[ScoredProduct], state: ConversationState) -> dict:
        """组装推荐响应"""
        device_name = state.device_type.value if state.device_type else "电脑"
        if not scored:
            return build_empty_response(device_name)

        # 从推荐器获取评分明细所需的元数据
        from ..db.product_repo import search_products
        meta = search_products(state.device_type or DeviceType.BOTH,
                               brands=state.constraints.get("brands", []))
        sbs = build_score_breakdowns(scored, meta)

        return {
            "type": "recommendation",
            "summary": "",
            "products": build_table_data(scored, sbs),
            "charts": {"price_bar": build_price_chart(scored), "radar": build_radar_chart(scored)},
            "device_type": device_name,
            "followup_hints": build_followup_hints(device_name),
        }

