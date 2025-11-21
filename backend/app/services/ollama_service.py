import httpx
from typing import Any, Dict, Optional

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434/api/generate", model: str = "llama3.1:8b"):
        self.base_url = base_url
        self.model = model

    async def chat(self, prompt: str, system: Optional[str] = None, timeout: float = 60.0) -> str:
        import logging
        payload = {
            "model": self.model,
            "prompt": prompt,
        }
        if system:
            payload["system"] = system
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, timeout=timeout)
            response.raise_for_status()
            raw_content = response.text
            logging.info(f"Ollama raw response: {raw_content}")
            # Handle streaming/multi-line JSON
            import json
            last_response = ""
            for line in raw_content.splitlines():
                try:
                    data = json.loads(line)
                    if "response" in data:
                        last_response = data["response"]
                except Exception:
                    continue
            return last_response

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        嘗試將 LLM 回應解析為 JSON 格式，若失敗則回傳空 dict。
        """
        import json
        try:
            return json.loads(response)
        except Exception:
            return {}
