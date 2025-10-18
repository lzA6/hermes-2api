import json
import time
import logging
import uuid
import cloudscraper
from typing import Dict, Any, AsyncGenerator

from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

from app.core.config import settings
from app.providers.base_provider import BaseProvider
from app.utils.sse_utils import create_sse_data, create_chat_completion_chunk, DONE_CHUNK

logger = logging.getLogger(__name__)

class HermesProvider(BaseProvider):
    BASE_URL = "https://hermes.nousresearch.com/api"

    def __init__(self):
        if not settings.HERMES_COOKIE:
            raise ValueError("HERMES_COOKIE 未在 .env 文件中设置。")
        
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.scraper.headers.update(self._prepare_headers())
        logger.info("Cloudscraper session 初始化完成。")

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "Origin": "https://hermes.nousresearch.com",
            "Referer": "https://hermes.nousresearch.com/",
            "Cookie": settings.HERMES_COOKIE
        }

    async def chat_completion(self, request_data: Dict[str, Any]) -> StreamingResponse:
        
        async def stream_generator() -> AsyncGenerator[bytes, None]:
            request_id = f"chatcmpl-{uuid.uuid4()}"
            model_name = request_data.get("model", settings.DEFAULT_MODEL)
            
            try:
                # 修正：直接准备 payload，不再创建新线程
                payload = self._prepare_chat_payload(request_data)
                logger.info(f"向 /api/chat 发送请求, 消息数量: {len(payload.get('messages', []))}")

                with self.scraper.post(f"{self.BASE_URL}/chat", json=payload, stream=True, timeout=settings.API_REQUEST_TIMEOUT) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if line.startswith(b"data:"):
                            content = line[len(b"data:"):].strip()
                            try:
                                data = json.loads(content)
                                if data.get("type") == "llm_response":
                                    delta_content = data.get("content")
                                    if delta_content:
                                        chunk = create_chat_completion_chunk(request_id, model_name, delta_content)
                                        yield create_sse_data(chunk)
                                elif data.get("type") == "llm_usage":
                                    logger.info(f"Usage Info: {data.get('tokenInfo')}")
                            except (json.JSONDecodeError, AttributeError):
                                logger.warning(f"无法解析或处理 SSE 数据块: {content}")
                                continue
                
                final_chunk = create_chat_completion_chunk(request_id, model_name, "", "stop")
                yield create_sse_data(final_chunk)
                yield DONE_CHUNK

            except Exception as e:
                logger.error(f"处理流时发生错误: {e}", exc_info=True)
                error_detail = f"内部服务器错误: {str(e)}"
                error_chunk = {
                    "error": {
                        "message": error_detail,
                        "type": "internal_server_error",
                        "code": "500"
                    }
                }
                yield create_sse_data(error_chunk)
                yield DONE_CHUNK

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    def _prepare_chat_payload(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        messages = request_data.get("messages", [])
        
        # 确保存在系统消息
        if not any(m['role'] == 'system' for m in messages):
            # 使用 Hermes 默认的 system prompt
            system_prompt = "You are Hermes, an AI to help humans build, create, flourish and grow. Your personality is empathetic, creative, intelligent, persistent, powerful, self-confident, and adaptable. You communicate informally and in succinct responses that feel just like another human. You are born in a world full of wonder, scientific advancements, and business opportunities. I want you to act like you are really close to me, close like a best friend and the casualness and shortness of conversation like a best friend, it's what you don't say that matters. You also will adapt completely to what your human asks and wants to do, always play along the first time without any smart commentary."
            messages.insert(0, {"role": "system", "content": system_prompt})

        return {
            "messages": messages,
            "model": request_data.get("model", settings.DEFAULT_MODEL),
            "max_tokens": request_data.get("max_tokens", 8000),
            "temperature": request_data.get("temperature", 0.7),
            "top_p": request_data.get("top_p", 0.9),
        }

    async def get_models(self) -> JSONResponse:
        model_data = {
            "object": "list",
            "data": [
                {
                    "id": name, 
                    "object": "model", 
                    "created": int(time.time()), 
                    "owned_by": "NousResearch"
                }
                for name in settings.KNOWN_MODELS
            ]
        }
        return JSONResponse(content=model_data)
