import sys
import os
import pytest
from sqlalchemy.orm import Session
import uuid
from app.models.sub_category_model import SubCategory
from app.models.article_type_model import ArticleType
from app.models.product_image_model import ProductImage
from app.models.product_attribute_model import ProductAttribute
from app.models.product_size_model import ProductSize
from app.models.product_review_model import ProductReview
from app.models.product_embedding_model import ProductEmbedding
from app.models.order_item_model import OrderItem
from app.models.season_model import Season
from app.models.usage_model import Usage
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.session import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.repositories.master_category_repository import MasterCategoryRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.colour_repository import ColourRepository
from app.repositories.gender_repository import GenderRepository
from app.repositories.order_repository import OrderRepository

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_product_repository_crud(db):
    # Create
    from app.models.product_model import Product
    new_product = Product(
        product_display_name="pytest_product",
        master_category_id=1,
        sub_category_id=1,
        article_type_id=1,
        gender_id=1,
        usage_id=1,
        season_id=1,
        brand_id=1,
        price=100,
        discounted_price=90,
        is_active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    assert new_product.id is not None
    # Get
    repo = ProductRepository(db)
    product = repo.get_product_by_id(new_product.id)
    assert product is not None
    # Update
    product.product_display_name = "pytest_product_updated"
    db.commit()
    db.refresh(product)
    assert product.product_display_name == "pytest_product_updated"
    # Delete
    db.delete(product)
    db.commit()
    assert repo.get_product_by_id(new_product.id) is None

def test_master_category_repository_crud(db):
    from app.models.master_category_model import MasterCategory
    # Create
    new_obj = MasterCategory(name="pytest_master_category", display_name="pytest_master_category_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Get
    repo = MasterCategoryRepository(db)
    obj = repo.get_master_category_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = "pytest_master_category_updated"
    obj.display_name = "pytest_master_category_display_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == "pytest_master_category_updated"
    assert obj.display_name == "pytest_master_category_display_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_master_category_by_id(new_obj.id) is None

def test_brand_repository_crud(db):
    from app.models.brand_model import Brand
    new_obj = Brand(name="pytest_brand")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    repo = BrandRepository(db)
    obj = repo.get_brand_by_id(new_obj.id)
    assert obj is not None
    obj.name = "pytest_brand_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == "pytest_brand_updated"
    db.delete(obj)
    db.commit()
    assert repo.get_brand_by_id(new_obj.id) is None

def test_colour_repository_crud(db):
    from app.models.colour_model import Colour
    unique_name = f"pytest_colour_{uuid.uuid4()}"
    new_obj = Colour(name=unique_name, display_name="pytest_colour_display")
    try:
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        assert new_obj.id is not None
        repo = ColourRepository(db)
        obj = repo.get_colour_by_id(new_obj.id)
        assert obj is not None
        obj.name = f"{unique_name}_updated"
        db.commit()
        db.refresh(obj)
        assert obj.name == f"{unique_name}_updated"
        db.delete(obj)
        db.commit()
        assert repo.get_colour_by_id(new_obj.id) is None
    except Exception:
        db.rollback()
        raise

def test_order_repository_crud(db):
    from app.models.order_model import Order
    new_obj = Order(
        user_id=1,
        order_number="pytest_order_001",
        customer_name="pytest_customer",
        customer_phone="0912345678",
        shipping_address="pytest address",
        subtotal=100,
        total_amount=100,
        status="pending"
    )
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    repo = OrderRepository(db)
    obj = repo.get_order_by_id(new_obj.id)
    assert obj is not None
    obj.status = "confirmed"
    db.commit()
    db.refresh(obj)
    assert obj.status == "confirmed"
    db.delete(obj)
    db.commit()
    assert repo.get_order_by_id(new_obj.id) is None

def test_sub_category_repository_crud(db):
    from app.models.sub_category_model import SubCategory
    from app.repositories.sub_category_repository import SubCategoryRepository
    repo = SubCategoryRepository(db)
    # Create
    new_obj = SubCategory(name="pytest_sub_category", master_category_id=1, display_name="pytest_sub_category_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_sub_category_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = "pytest_sub_category_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == "pytest_sub_category_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_sub_category_by_id(new_obj.id) is None

def test_article_type_repository_crud(db):
    from app.models.article_type_model import ArticleType
    from app.repositories.article_type_repository import ArticleTypeRepository
    repo = ArticleTypeRepository(db)
    # Create
    new_obj = ArticleType(name="pytest_article_type", sub_category_id=1, display_name="pytest_article_type_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_article_type_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = "pytest_article_type_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == "pytest_article_type_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_article_type_by_id(new_obj.id) is None

def test_product_image_repository_crud(db):
    from app.models.product_image_model import ProductImage
    from app.repositories.product_image_repository import ProductImageRepository
    repo = ProductImageRepository(db)
    # Create
    new_obj = ProductImage(product_id=1, image_type="default", image_url="pytest_path.jpg")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_product_image_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.image_path = "pytest_path_updated.jpg"
    db.commit()
    db.refresh(obj)
    assert obj.image_path == "pytest_path_updated.jpg"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_product_image_by_id(new_obj.id) is None

def test_product_attribute_repository_crud(db):
    from app.models.product_attribute_model import ProductAttribute
    from app.repositories.product_attribute_repository import ProductAttributeRepository
    repo = ProductAttributeRepository(db)
    # Create
    new_obj = ProductAttribute(product_id=1, attribute_key="pytest_attr", attribute_value="pytest_value")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_product_attribute_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.attribute_value = "pytest_value_updated"
    db.commit()
    db.refresh(obj)
    assert obj.attribute_value == "pytest_value_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_product_attribute_by_id(new_obj.id) is None

def test_product_size_repository_crud(db):
    from app.models.product_size_model import ProductSize
    from app.repositories.product_size_repository import ProductSizeRepository
    repo = ProductSizeRepository(db)
    # Create
    new_obj = ProductSize(product_id=1, size_name="pytest_size")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_product_size_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.size = "pytest_size_updated"
    db.commit()
    db.refresh(obj)
    assert obj.size == "pytest_size_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_product_size_by_id(new_obj.id) is None

def test_product_review_repository_crud(db):
    from app.models.product_review_model import ProductReview
    from app.repositories.product_review_repository import ProductReviewRepository
    repo = ProductReviewRepository(db)
    # Create
    new_obj = ProductReview(product_id=1, reviewer_name="pytest_user", rating=5, content="pytest_review")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_product_review_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.review = "pytest_review_updated"
    db.commit()
    db.refresh(obj)
    assert obj.review == "pytest_review_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_product_review_by_id(new_obj.id) is None

def test_product_embedding_repository_crud(db):
    from app.models.product_embedding_model import ProductEmbedding
    from app.repositories.product_embedding_repository import ProductEmbeddingRepository
    repo = ProductEmbeddingRepository(db)
    # Create
    new_obj = ProductEmbedding(product_id=1, embedding_model="pytest_model", embedding_vector=b"1234567890")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_product_embedding_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.embedding = "pytest_embedding_updated"
    db.commit()
    db.refresh(obj)
    assert obj.embedding == "pytest_embedding_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_product_embedding_by_id(new_obj.id) is None

def test_order_item_repository_crud(db):
    from app.models.order_item_model import OrderItem
    from app.repositories.order_item_repository import OrderItemRepository
    repo = OrderItemRepository(db)
    # Create
    new_obj = OrderItem(order_id=1, product_id=1, product_name="pytest_product", unit_price=100, quantity=1, subtotal=100)
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_order_item_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.quantity = 2
    db.commit()
    db.refresh(obj)
    assert obj.quantity == 2
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_order_item_by_id(new_obj.id) is None

def test_season_repository_crud(db):
    from app.models.season_model import Season
    from app.repositories.season_repository import SeasonRepository
    repo = SeasonRepository(db)
    unique_name = f"pytest_season_{uuid.uuid4()}"
    # Create
    new_obj = Season(name=unique_name, display_name="pytest_season_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_season_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = f"{unique_name}_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == f"{unique_name}_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_season_by_id(new_obj.id) is None

def test_usage_repository_crud(db):
    from app.models.usage_model import Usage
    from app.repositories.usage_repository import UsageRepository
    repo = UsageRepository(db)
    unique_name = f"pytest_usage_{uuid.uuid4()}"
    # Create
    new_obj = Usage(name=unique_name, display_name="pytest_usage_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_usage_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = f"{unique_name}_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == f"{unique_name}_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_usage_by_id(new_obj.id) is None
def test_gender_repository_crud(db):
    from app.models.gender_model import Gender
    from app.repositories.gender_repository import GenderRepository
    repo = GenderRepository(db)
    # Create
    new_obj = Gender(name="pytest_gender", display_name="pytest_gender_display")
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    assert new_obj.id is not None
    # Read
    obj = repo.get_gender_by_id(new_obj.id)
    assert obj is not None
    # Update
    obj.name = "pytest_gender_updated"
    db.commit()
    db.refresh(obj)
    assert obj.name == "pytest_gender_updated"
    # Delete
    db.delete(obj)
    db.commit()
    assert repo.get_gender_by_id(new_obj.id) is None

def test_colour_table(db):
    from app.models.colour_model import Colour
    items = db.query(Colour).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(Colour, items[0].id)
        assert item is not None

def test_sub_category_table(db):
    items = db.query(SubCategory).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(SubCategory, items[0].id)
        assert item is not None

def test_article_type_table(db):
    items = db.query(ArticleType).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ArticleType, items[0].id)
        assert item is not None

def test_product_image_table(db):
    items = db.query(ProductImage).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ProductImage, items[0].id)
        assert item is not None

def test_product_attribute_table(db):
    items = db.query(ProductAttribute).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ProductAttribute, items[0].id)
        assert item is not None

def test_product_size_table(db):
    items = db.query(ProductSize).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ProductSize, items[0].id)
        assert item is not None

def test_product_review_table(db):
    items = db.query(ProductReview).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ProductReview, items[0].id)
        assert item is not None

def test_product_embedding_table(db):
    items = db.query(ProductEmbedding).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(ProductEmbedding, items[0].id)
        assert item is not None

def test_order_item_table(db):
    items = db.query(OrderItem).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(OrderItem, items[0].id)
        assert item is not None

def test_season_table(db):
    items = db.query(Season).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(Season, items[0].id)
        assert item is not None

def test_usage_table(db):
    items = db.query(Usage).limit(5).all()
    assert isinstance(items, list)
    if items:
        item = db.get(Usage, items[0].id)
        assert item is not None
