import sqlite3
import json
from tqdm import tqdm
from app.services.embedding_service import EmbeddingService  # ✅ 不再需要 backend 前綴

DB_PATH = "fashion_store.db"   # ✅ 直接在 backend 下找 DB
TABLE_NAME = "product_embeddings"
PRODUCT_TABLE = "products"

# 建立 product_embeddings 資料表 (如尚未存在)
def create_embeddings_table(conn):
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            product_id INTEGER PRIMARY KEY,
            embedding TEXT NOT NULL
        )
    """)
    conn.commit()

# 讀取所有商品資料
def fetch_products(conn):
    cursor = conn.execute("""
        SELECT p.id,
               p.product_display_name,
               at.name AS article_type,
               c.name AS base_colour,
               s.name AS season,
               u.name AS usage
        FROM products p
        LEFT JOIN article_types at ON p.article_type_id = at.id
        LEFT JOIN colours c ON p.base_colour_id = c.id
        LEFT JOIN seasons s ON p.season_id = s.id
        LEFT JOIN usages u ON p.usage_id = u.id
    """)
    return cursor.fetchall()

# 組合商品描述文字
def build_text(row):
    # row: (id, product_display_name, article_type, base_colour, season, usage)
    return " ".join([str(x) for x in row[1:] if x])

# 批次生成並儲存向量
def main():
    conn = sqlite3.connect(DB_PATH)
    products = fetch_products(conn)
    texts = [build_text(row) for row in products]
    product_ids = [row[0] for row in products]

    embedder = EmbeddingService()
    print(f"Generating embeddings for {len(products)} products...")
    vectors = embedder.batch_encode(texts)

    for product_id, text, vector in tqdm(zip(product_ids, texts, vectors), total=len(product_ids), desc="Embedding products"):
        embedding_json = json.dumps(vector)  # 向量序列化成 JSON
        conn.execute(
            f"""REPLACE INTO {TABLE_NAME} 
                (product_id, embedding_model, embedding_vector, embedding_text) 
                VALUES (?, ?, ?, ?)""",
            (product_id, "your_model_name", sqlite3.Binary(embedding_json.encode("utf-8")), text),
        )
    conn.commit()
    conn.close()
    print("All product embeddings generated and saved.")

if __name__ == "__main__":
    main()
