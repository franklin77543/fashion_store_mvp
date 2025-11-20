"""
初始化資料庫，import 所有 models 並建立所有資料表
"""
from app.db.session import Base, engine
# Import all models to register them with SQLAlchemy
from app.models.brand_model import Brand
from app.models.colour_model import Colour
from app.models.gender_model import Gender
from app.models.master_category_model import MasterCategory
from app.models.order_item_model import OrderItem
from app.models.order_model import Order
from app.models.product_attribute_model import ProductAttribute
from app.models.product_embedding_model import ProductEmbedding
from app.models.product_image_model import ProductImage
from app.models.product_model import Product
from app.models.product_review_model import ProductReview
from app.models.product_size_model import ProductSize
from app.models.season_model import Season
from app.models.sub_category_model import SubCategory
from app.models.usage_model import Usage
from app.models.article_type_model import ArticleType

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All tables created.")
