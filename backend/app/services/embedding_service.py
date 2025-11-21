from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> List[float]:
        """
        將單句文字轉換為語義向量 (list[float])
        """
        return self.model.encode(text).tolist()

    def batch_encode(self, texts: List[str]) -> List[List[float]]:
        """
        批次將多句文字轉換為語義向量 (list[list[float]])
        """
        return [vec.tolist() for vec in self.model.encode(texts)]
