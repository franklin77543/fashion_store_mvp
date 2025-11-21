from typing import Dict, Any, Optional
from .ollama_service import OllamaService

class NLUService:
    def __init__(self, ollama_service: Optional[OllamaService] = None):
        self.ollama_service = ollama_service or OllamaService()

    async def parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        解析使用者自然語言查詢，返回 intentType, entities, filters。
        會呼叫 Ollama LLM 進行語意解析。
        """
        prompt = (
            "請將以下使用者查詢解析為 JSON 格式，包含 intentType, entities, filters。"
            "\n查詢: '" + user_input + "'"
            "\n請回傳格式: {\"intentType\": str, \"entities\": list, \"filters\": dict}"
        )
        response = await self.ollama_service.chat(prompt)
        result = self.ollama_service.parse_json_response(response)
        # 若解析失敗，回傳預設格式
        if not isinstance(result, dict):
            result = {"intentType": "unknown", "entities": [], "filters": {}}
        return result
