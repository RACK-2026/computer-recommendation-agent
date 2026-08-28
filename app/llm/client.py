"""LLM API 客户端封装"""
from typing import Optional, List, Dict, AsyncGenerator
from openai import AsyncOpenAI
from ..config import settings


class LLMClient:
    """OpenAI SDK 封装，兼容 DeepSeek / OpenAI / Qwen 等 API"""

    def __init__(self):
        # Allow the API server and health endpoint to start before credentials
        # are configured. LLM calls will return an actionable error instead.
        self.client = None
        if settings.llm_api_key:
            self.client = AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url,
            )
        self.model = settings.llm_model

    def _require_client(self) -> AsyncOpenAI:
        if self.client is None:
            raise RuntimeError(
                "LLM is not configured. Copy .env.example to .env and set LLM_API_KEY."
            )
        return self.client

    async def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.3,
        max_tokens: int = 2048,
        response_format: Optional[Dict] = None,
    ) -> str:
        """非流式对话"""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format

        try:
            resp = await self._require_client().chat.completions.create(**kwargs)
            return resp.choices[0].message.content or ""
        except Exception as e:
            raise Exception(f"LLM API 调用失败: {str(e)}")

    async def chat_stream(
        self,
        messages: List[Dict],
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[str, None]:
        """流式对话"""
        try:
            stream = await self._require_client().chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"LLM 流式调用失败: {str(e)}")

    async def extract_json(
        self,
        messages: List[Dict],
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        """强制 JSON 格式输出，不支持 response_format 的 API 自动降级"""
        try:
            try:
                resp = await self._require_client().chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"},
                )
                return resp.choices[0].message.content or "{}"
            except Exception as json_err:
                # 降级：不用 response_format，改在 prompt 里要求 JSON（先复制避免修改原消息）
                fallback_messages = [dict(m) if isinstance(m, dict) else m for m in messages]
                if fallback_messages and isinstance(fallback_messages[-1], dict):
                    fallback_messages[-1]["content"] = fallback_messages[-1].get("content", "") + "\n\n请严格只输出 JSON，不要包含其他文字。"
                resp = await self._require_client().chat.completions.create(
                    model=self.model,
                    messages=fallback_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return resp.choices[0].message.content or "{}"
        except Exception as e:
            raise Exception(f"LLM JSON 调用失败: {str(e)}")


# 全局单例
llm_client = LLMClient()

