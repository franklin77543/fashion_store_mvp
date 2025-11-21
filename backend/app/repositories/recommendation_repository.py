import sqlite3
import json
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.config import settings

DB_PATH = settings.DB_PATH


class RecommendationRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def exact_search(self, entities: Dict[str, Any], limit: int = 10) -> List[int]:
        """
        根據 entities (如顏色、類型等) 精確搜尋商品 id
        """
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id FROM products WHERE 1=1"
        params = []
        for key, value in entities.items():
            query += f" AND {key}=?"
            params.append(value)
        query += " LIMIT ?"
        params.append(limit)
        cursor = conn.execute(query, params)
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results

    def semantic_search(self, query_vector: List[float], top_k: int = 10) -> List[int]:
        """
        根據語義向量搜尋最相近商品 id (餘弦相似度)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT product_id, embedding_vector FROM product_embeddings")
        product_ids = []
        embeddings = []
        for row in cursor:
            product_ids.append(row[0])
            embeddings.append(json.loads(row[1]))
        conn.close()
        # 計算餘弦相似度
        query_vec = np.array(query_vector)
        emb_matrix = np.array(embeddings)
        scores = emb_matrix @ query_vec / (np.linalg.norm(emb_matrix, axis=1) * np.linalg.norm(query_vec) + 1e-8)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [product_ids[i] for i in top_indices]

    def style_based_search(self, filters: Dict[str, Any], limit: int = 10) -> List[int]:
        """
        根據風格/條件 (如季節、場合) 搜尋商品 id
        """
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id FROM products WHERE 1=1"
        params = []
        for key, value in filters.items():
            query += f" AND {key}=?"
            params.append(value)
        query += " LIMIT ?"
        params.append(limit)
        cursor = conn.execute(query, params)
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
