
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.product_api import router as product_router
from app.api.category_api import router as category_router
from app.api.recommendation_api import router as recommendation_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Fashion Store API")

# 加入 CORS 設定，允許所有來源跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(recommendation_router)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

app.mount("/images", StaticFiles(directory="../fashion-dataset/images"), name="images")
