from fastapi import FastAPI
from app.api.product_api import router as product_router
from app.api.category_api import router as category_router

app = FastAPI(title="Fashion Store API")

app.include_router(product_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
