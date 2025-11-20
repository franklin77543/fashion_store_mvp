import pytest
from sqlalchemy import text
from app.db.session import SessionLocal
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductDetail, ProductBase
from app.services.brand_service import BrandService
from app.services.colour_service import ColourService
from app.services.gender_service import GenderService
from app.services.master_category_service import MasterCategoryService
from app.services.order_service import OrderService
from app.services.order_item_service import OrderItemService
from app.services.product_attribute_service import ProductAttributeService
from app.services.product_embedding_service import ProductEmbeddingService
from app.services.product_image_service import ProductImageService
from app.services.product_review_service import ProductReviewService
from app.services.product_size_service import ProductSizeService
from app.services.season_service import SeasonService
from app.services.sub_category_service import SubCategoryService
from app.services.usage_service import UsageService
from app.schemas.product_attribute_schema import ProductAttributeCreate, ProductAttributeUpdate

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

    repo = ProductRepository(db)
    service = ProductService(repo)
    # create
    from app.schemas.product_schema import ProductCreate, ProductUpdate
    data = ProductCreate(
        product_display_name="test_product",
        gender_id=1,
        master_category_id=1,
        sub_category_id=1,
        article_type_id=1,
        base_colour_id=1,
        season_id=1,
        year=2025,
        usage_id=1,
        brand_id=1,
        price=100.0,
        discounted_price=90.0,
        discount_percent=10.0,
        is_active=True,
        stock_count=10,
        rating=5.0,
        review_count=1,
        view_count=1
    )
    product = service.create_product(data)
    assert product.product_display_name == "test_product"
    # update
    updated = service.update_product(product.id, ProductUpdate(product_display_name="updated_product", is_active=True))
    assert updated.product_display_name == "updated_product"
    # get
    got = service.get_product_detail(product.id)
    assert got.product_display_name == "updated_product"
    # list
    products = service.list_products()
    assert any(p.product_display_name == "updated_product" for p in products)
    # delete
    service.delete_product(product.id)
    assert service.get_product_detail(product.id) is None

def test_brand_service_crud(db):
    from app.repositories.brand_repository import BrandRepository
    from app.services.brand_service import BrandService
    from app.schemas.brand_schema import BrandCreate, BrandUpdate
    repo = BrandRepository(db)
    service = BrandService(repo)
    # create
    data = BrandCreate(name="test_brand", display_name="Test")
    brand = service.create_brand(data)
    assert brand.name == "test_brand"
    # update
    updated = service.update_brand(brand.id, BrandUpdate(name="updated_brand", display_name="Updated"))
    assert updated.name == "updated_brand"
    # get
    got = service.get_brand(brand.id)
    assert got.name == "updated_brand"
    # list
    brands = service.list_brands()
    assert any(b.name == "updated_brand" for b in brands)
    # delete
    service.delete_brand(brand.id)
    assert service.get_brand(brand.id) is None

def test_colour_service_crud(db):
    from app.repositories.colour_repository import ColourRepository
    from app.services.colour_service import ColourService
    from app.schemas.colour_schema import ColourCreate, ColourUpdate
    repo = ColourRepository(db)
    service = ColourService(repo)
    # create
    data = ColourCreate(name="test_colour", display_name="Test")
    colour = service.create_colour(data)
    assert colour.name == "test_colour"
    # update
    updated = service.update_colour(colour.id, ColourUpdate(name="updated_colour", display_name="Updated"))
    assert updated.name == "updated_colour"
    # get
    got = service.get_colour(colour.id)
    assert got.name == "updated_colour"
    # list
    colours = service.list_colours()
    assert any(c.name == "updated_colour" for c in colours)
    # delete
    service.delete_colour(colour.id)
    assert service.get_colour(colour.id) is None

def test_gender_service_crud(db):
    from app.repositories.gender_repository import GenderRepository
    from app.services.gender_service import GenderService
    from app.schemas.gender_schema import GenderCreate, GenderUpdate
    repo = GenderRepository(db)
    service = GenderService(repo)
    # create
    data = GenderCreate(name="test_gender", display_name="Test")
    gender = service.create_gender(data)
    assert gender.name == "test_gender"
    # update
    updated = service.update_gender(gender.id, GenderUpdate(name="updated_gender", display_name="Updated"))
    assert updated.name == "updated_gender"
    # get
    got = service.get_gender(gender.id)
    assert got.name == "updated_gender"
    # list
    genders = service.list_genders()
    assert any(g.name == "updated_gender" for g in genders)
    # delete
    service.delete_gender(gender.id)
    assert service.get_gender(gender.id) is None

def test_master_category_service_crud(db):
    from app.repositories.master_category_repository import MasterCategoryRepository
    from app.services.master_category_service import MasterCategoryService
    from app.schemas.master_category_schema import MasterCategory, MasterCategoryCreate, MasterCategoryUpdate
    repo = MasterCategoryRepository(db)
    service = MasterCategoryService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM master_categories"))
    db.commit()
    # create
    data = MasterCategoryCreate(name="test_category", display_name="Test")
    category = service.create_master_category(data)
    assert category.name == "test_category"
    # update
    updated = service.update_master_category(category.id, MasterCategoryUpdate(name="updated_category", display_name="Updated"))
    assert updated.name == "updated_category"
    # get
    got = service.get_master_category(category.id)
    assert got.name == "updated_category"
    # list
    categories = service.list_master_categories()
    assert any(c.name == "updated_category" for c in categories)
    # delete
    service.delete_master_category(category.id)
    assert service.get_master_category(category.id) is None

def test_order_service_crud(db):
    from app.repositories.order_repository import OrderRepository
    from app.services.order_service import OrderService
    from app.schemas.order_schema import OrderBase
    repo = OrderRepository(db)
    service = OrderService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM orders"))
    db.commit()
    # create
    from app.schemas.order_schema import OrderCreate, OrderUpdate
    data = OrderCreate(
        user_id=1,
        order_number="ORD123",
        customer_name="Test User",
        customer_email="test@example.com",
        customer_phone="1234567890",
        shipping_address="Test Address",
        subtotal=100.0,
        shipping_fee=10.0,
        discount_amount=0.0,
        total_amount=110.0,
        status="pending",
        payment_status="unpaid",
        payment_method="credit_card",
        customer_note="note",
        admin_note="admin"
    )
    order = service.create_new_order(data.model_dump())
    assert order.status == "pending"
    # update
    updated = service.update_order(order.id, OrderUpdate(status="completed"))
    assert updated.status == "completed"
    # get
    got = service.get_order_detail(order.id)
    assert got.status == "completed"
    # delete
    service.delete_order(order.id)
    assert service.get_order_detail(order.id) is None

def test_order_item_service_crud(db):
    from app.repositories.order_item_repository import OrderItemRepository
    from app.services.order_item_service import OrderItemService
    from app.schemas.order_item_schema import OrderItemCreate, OrderItemUpdate
    repo = OrderItemRepository(db)
    service = OrderItemService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM order_items"))
    db.commit()
    # create
    data = OrderItemCreate(order_id=1, product_id=1, product_name="test_item", unit_price=10, quantity=1, subtotal=10)
    item = service.create_order_item(data)
    assert item.product_name == "test_item"
    # update
    updated = service.update_order_item(item.id, OrderItemUpdate(product_name="updated_item"))
    assert updated.product_name == "updated_item"
    # get
    got = service.get_order_item(item.id)
    assert got.product_name == "updated_item"
    # list
    items = service.list_order_items()
    assert any(i.product_name == "updated_item" for i in items)
    # delete
    service.delete_order_item(item.id)
    assert service.get_order_item(item.id) is None

def test_product_attribute_service_crud(db):
    from app.repositories.product_attribute_repository import ProductAttributeRepository
    from app.services.product_attribute_service import ProductAttributeService
    from app.schemas.product_attribute_schema import ProductAttributeCreate, ProductAttributeUpdate
    repo = ProductAttributeRepository(db)
    service = ProductAttributeService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM product_attributes"))
    db.commit()
    # create
    data = ProductAttributeCreate(product_id=1, attribute_key="test", attribute_value="value")
    attr = service.create_attribute(data)
    assert attr.attribute_key == "test"
    # update
    updated = service.update_attribute(attr.id, ProductAttributeUpdate(attribute_key="updated", attribute_value="updated"))
    assert updated.attribute_key == "updated"
    # get
    got = service.get_attribute(attr.id)
    assert got.attribute_key == "updated"
    # list
    attrs = service.list_attributes()
    assert any(a.attribute_key == "updated" for a in attrs)
    # delete
    service.delete_attribute(attr.id)
    assert service.get_attribute(attr.id) is None

def test_product_embedding_service_crud(db):
    from app.repositories.product_embedding_repository import ProductEmbeddingRepository
    from app.services.product_embedding_service import ProductEmbeddingService
    from app.schemas.product_embedding_schema import ProductEmbeddingCreate, ProductEmbeddingUpdate
    repo = ProductEmbeddingRepository(db)
    service = ProductEmbeddingService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM product_embeddings"))
    db.commit()
    # create
    data = ProductEmbeddingCreate(product_id=1, embedding_model="test_model", embedding_vector=b"123", embedding_text="test_vec")
    embedding = service.create_product_embedding(data)
    assert embedding.embedding_model == "test_model"
    # update
    updated = service.update_product_embedding(embedding.id, ProductEmbeddingUpdate(embedding_model="updated_model"))
    assert updated.embedding_model == "updated_model"
    # get
    got = service.get_product_embedding(embedding.id)
    assert got.embedding_model == "updated_model"
    # list
    embeddings = service.list_product_embeddings()
    assert any(e.embedding_model == "updated_model" for e in embeddings)
    # delete
    service.delete_product_embedding(embedding.id)
    assert service.get_product_embedding(embedding.id) is None

def test_product_image_service_crud(db):
    from app.repositories.product_image_repository import ProductImageRepository
    from app.services.product_image_service import ProductImageService
    from app.schemas.product_image_schema import ProductImageCreate, ProductImageUpdate
    repo = ProductImageRepository(db)
    service = ProductImageService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM product_images"))
    db.commit()
    # create
    data = ProductImageCreate(product_id=1, image_type="main", image_url="url", resolution="1080x1440", is_primary=True, display_order=1)
    image = service.create_product_image(data)
    assert image.image_type == "main"
    # update
    updated = service.update_product_image(image.id, ProductImageUpdate(image_type="updated_type"))
    assert updated.image_type == "updated_type"
    # get
    got = service.get_product_image(image.id)
    assert got.image_type == "updated_type"
    # list
    images = service.list_product_images()
    assert any(i.image_type == "updated_type" for i in images)
    # delete
    service.delete_product_image(image.id)
    assert service.get_product_image(image.id) is None

def test_product_review_service_crud(db):
    from app.repositories.product_review_repository import ProductReviewRepository
    from app.services.product_review_service import ProductReviewService
    from app.schemas.product_review_schema import ProductReviewCreate, ProductReviewUpdate
    repo = ProductReviewRepository(db)
    service = ProductReviewService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM product_reviews"))
    db.commit()
    # create
    data = ProductReviewCreate(product_id=1, reviewer_name="tester", reviewer_email="test@example.com", rating=5, title="Great", content="good", is_verified=True, is_approved=True, helpful_count=1)
    review = service.create_product_review(data)
    assert review.reviewer_name == "tester"
    # update
    updated = service.update_product_review(review.id, ProductReviewUpdate(reviewer_name="updated"))
    assert updated.reviewer_name == "updated"
    # get
    got = service.get_product_review(review.id)
    assert got.reviewer_name == "updated"
    # list
    reviews = service.list_product_reviews()
    assert any(r.reviewer_name == "updated" for r in reviews)
    # delete
    service.delete_product_review(review.id)
    assert service.get_product_review(review.id) is None

def test_product_size_service_crud(db):
    from app.repositories.product_size_repository import ProductSizeRepository
    from app.services.product_size_service import ProductSizeService
    from app.schemas.product_size_schema import ProductSizeCreate, ProductSizeUpdate
    repo = ProductSizeRepository(db)
    service = ProductSizeService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM product_sizes"))
    db.commit()
    # create
    data = ProductSizeCreate(product_id=1, size_name="M", stock_count=10, is_available=True)
    size = service.create_product_size(data)
    assert size.size_name == "M"
    # update
    updated = service.update_product_size(size.id, ProductSizeUpdate(size_name="L"))
    assert updated.size_name == "L"
    # get
    got = service.get_product_size(size.id)
    assert got.size_name == "L"
    # list
    sizes = service.list_product_sizes()
    assert any(s.size_name == "L" for s in sizes)
    # delete
    service.delete_product_size(size.id)
    assert service.get_product_size(size.id) is None

def test_season_service_crud(db):
    from app.repositories.season_repository import SeasonRepository
    from app.services.season_service import SeasonService
    from app.schemas.season_schema import SeasonCreate, SeasonUpdate
    repo = SeasonRepository(db)
    service = SeasonService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM seasons"))
    db.commit()
    # create
    data = SeasonCreate(name="test_season", display_name="Test")
    season = service.create_season(data)
    assert season.name == "test_season"
    # update
    updated = service.update_season(season.id, SeasonUpdate(name="updated_season", display_name="Updated"))
    assert updated.name == "updated_season"
    # get
    got = service.get_season(season.id)
    assert got.name == "updated_season"
    # list
    seasons = service.list_seasons()
    assert any(s.name == "updated_season" for s in seasons)
    # delete
    service.delete_season(season.id)
    assert service.get_season(season.id) is None

def test_sub_category_service_crud(db):
    from app.repositories.sub_category_repository import SubCategoryRepository
    from app.services.sub_category_service import SubCategoryService
    from app.schemas.sub_category_schema import SubCategoryCreate, SubCategoryUpdate
    repo = SubCategoryRepository(db)
    service = SubCategoryService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM sub_categories"))
    db.commit()
    # create
    data = SubCategoryCreate(name="test_sub", master_category_id=1, display_name="Test")
    sub = service.create_sub_category(data)
    assert sub.name == "test_sub"
    # update
    updated = service.update_sub_category(sub.id, SubCategoryUpdate(name="updated_sub"))
    assert updated.name == "updated_sub"
    # get
    got = service.get_sub_category(sub.id)
    assert got.name == "updated_sub"
    # list
    subs = service.list_sub_categories()
    assert any(s.name == "updated_sub" for s in subs)
    # delete
    service.delete_sub_category(sub.id)
    assert service.get_sub_category(sub.id) is None

def test_usage_service_crud(db):
    from app.repositories.usage_repository import UsageRepository
    from app.services.usage_service import UsageService
    from app.schemas.usage_schema import UsageCreate, UsageUpdate
    repo = UsageRepository(db)
    service = UsageService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM usages"))
    db.commit()
    # create
    data = UsageCreate(name="test_usage", display_name="Test")
    usage = service.create_usage(data)
    assert usage.name == "test_usage"
    # update
    updated = service.update_usage(usage.id, UsageUpdate(name="updated_usage"))
    assert updated.name == "updated_usage"
    # get
    got = service.get_usage(usage.id)
    assert got.name == "updated_usage"
    # list
    usages = service.list_usages()
    assert any(u.name == "updated_usage" for u in usages)
    # delete
    service.delete_usage(usage.id)
    assert service.get_usage(usage.id) is None
def test_article_type_service_crud(db):
    from app.repositories.article_type_repository import ArticleTypeRepository
    from app.services.article_type_service import ArticleTypeService
    from app.schemas.article_type_schema import ArticleTypeCreate, ArticleTypeUpdate
    repo = ArticleTypeRepository(db)
    service = ArticleTypeService(repo)
    # 清理資料表，避免唯一欄位衝突
    db.execute(text("DELETE FROM article_types"))
    db.commit()
    # create
    data = ArticleTypeCreate(name="test_type", sub_category_id=1, display_name="Test")
    article_type = service.create_article_type(data)
    assert article_type.name == "test_type"
    # update
    updated = service.update_article_type(article_type.id, ArticleTypeUpdate(name="updated_type"))
    assert updated.name == "updated_type"
    # get
    got = service.get_article_type(article_type.id)
    assert got.name == "updated_type"
    # list
    types = service.list_article_types()
    assert any(t.name == "updated_type" for t in types)
    # delete
    service.delete_article_type(article_type.id)
    assert service.get_article_type(article_type.id) is None
