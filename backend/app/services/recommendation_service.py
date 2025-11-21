from typing import List, Dict, Any
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.nlu_service import NLUService
from app.services.embedding_service import EmbeddingService
from app.services.ollama_service import OllamaService

class RecommendationService:
    def __init__(self,
                 repo: RecommendationRepository = None,
                 nlu: NLUService = None,
                 embedder: EmbeddingService = None,
                 ollama: OllamaService = None):
        self.repo = repo or RecommendationRepository()
        self.nlu = nlu or NLUService()
        self.embedder = embedder or EmbeddingService()
        self.ollama = ollama or OllamaService()

    async def recommend(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        主要推薦邏輯：
        1. 呼叫 NLU Service 解析意圖
        2. 根據意圖類型選擇搜尋策略
        3. 呼叫對應的 Repository 方法
        4. 生成推薦理由 (使用 LLM)
        5. 返回推薦商品列表
        """
        intent = await self.nlu.parse_intent(query)
        intent_type = intent.get("intentType", "unknown")
        entities = intent.get("entities", {})
        filters = intent.get("filters", {})
        product_ids = []
        match_scores = []

        if intent_type == "exact":
            product_ids = self.repo.exact_search(entities, limit)
            match_scores = [1.0] * len(product_ids)
        elif intent_type == "semantic":
            query_vec = self.embedder.encode(query)
            product_ids = self.repo.semantic_search(query_vec, limit)
            match_scores = [1.0] * len(product_ids)  # 可進一步計算相似度
        elif intent_type == "style":
            product_ids = self.repo.style_based_search(filters, limit)
            match_scores = [1.0] * len(product_ids)
        else:
            # fallback: semantic search
            query_vec = self.embedder.encode(query)
            product_ids = self.repo.semantic_search(query_vec, limit)
            match_scores = [1.0] * len(product_ids)

        # 生成推薦理由 (可用 LLM)
        reason_prompt = f"請為查詢 '{query}' 生成推薦理由，並以簡短中文說明。"
        reason = await self.ollama.chat(reason_prompt)

        # 組合回傳格式
        recommendations = []
        for pid, score in zip(product_ids, match_scores):
            recommendations.append({
                "product_id": pid,
                "matchScore": score,
                "reason": reason
            })
        return recommendations
